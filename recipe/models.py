import logging
from django.db import connection
from typing import cast
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import FloatField, PositiveBigIntegerField
from recipe.matching import closest_str
import re
import itertools

# Create your models here.
class Recipe(models.Model):
    id = models.AutoField
    title = models.CharField(max_length = 120)
    description = models.TextField()
    def __str__(self) -> str:
        return self.title
    def save(self, *args, **kwargs):
        saved_recipe = super().save(*args, **kwargs)
        DetailedRecipe().save( desc = self.description, origin = self)
        return saved_recipe


class DetailedRecipe(models.Model):
    origin_id = models.OneToOneField(Recipe, on_delete=models.CASCADE,primary_key= True, default=-1)
    ingredients_list = models.TextField()
    calories = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.ingredients_list

    def save(self, desc,origin, *args, **kwargs):
        self.origin_id = origin
        self.ingredients_list = desc

        for ingredient in  single_ingredients(self.ingredients_list):
            weight = get_weight(ingredient)#remove weight into separate value
            try:
                fdc_id = get_fdc_id_from_description(get_ingredient_from_database(remove_weight(ingredient)))
                ingredient_calories = CalculateCalories(str(fdc_id),weight)
                self.calories += ingredient_calories
                logging.warning("Calories from %s: %i", ingredient, ingredient_calories)
            except NoSuchEntryError:
                logging.warning("No database match found for %s, no calories derived from that ingredient.", ingredient)
                pass
        saved_recipe = super().save(force_insert= True)
        return saved_recipe

class NoSuchEntryError(Exception):
    def __init__(self,input_string,error_string = "ERROR: No matching entry found in database for "):
        self.input_string = input_string
        self.error_message = error_string + input_string
        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message


def get_fdc_id_from_description(description):
    with connection.cursor() as cursor:
        query = "SELECT fdc_id FROM dbo.food WHERE description = '"+description+"'"
        logging.warning(query)
        cursor.execute(query)
        results = cursor.fetchone()
    return results[0]

def get_weight(ingredient_string:str):
    components = re.split(' |,',ingredient_string.strip())
    weight_string = components[-1]
    weight_string = re.sub('[^0-9,\.]', "", weight_string) #remove non-digit chars
    return float(weight_string)

#removes weight from ingredient string. Ex. 'onions, chopped, 100g' -> onions, chopped
def remove_weight(ingredient_string):
    size = len(ingredient_string)
    weight = get_weight(ingredient_string)
    if weight.is_integer():
        weight_size = len(str(weight))
    else:
        weight_size = len(str(weight))+1
    return ingredient_string[:size -weight_size].strip()

# expects ex "onion, 100g \n cooked potato 500g"
def single_ingredients(ingredient_list):
    ingredients = re.split("\r|\n",ingredient_list)
    while '' in ingredients:
        ingredients.remove('')
    return ingredients

#wrapper for get_matching_ingredients_from_database, chooses closest match
def get_ingredient_from_database(ingredient:str):
    result = closest_str(ingredient, get_matching_ingredients_from_database(ingredient))
    logging.warning("Closest match to %s chosesn as %s",ingredient,result)
    return result

#expects ingredient components to be separated by spaces or commas. Returns list of tuples (description, fdc_id)
def get_matching_ingredients_from_database(ingredient:str):
    if ingredient =='':
        raise NoSuchEntryError("Ingredient reduced to 0 length with no matches")
    component_list = re.split(' |,',ingredient)
    while '' in component_list:
        component_list.remove('')
    contains_query = ''
    first = True
    for component in component_list:
        if first:
            contains_query += "description LIKE '%"+component+"%'"#" contains(description, '"+component+"')"
            first = False
        else:
            contains_query += "AND description LIKE '%"+component+"%'"#"AND contains(description, '"+component+"')"
    with connection.cursor() as cursor:
        query = 'SELECT TOP (1000) description, fdc_id FROM dbo.food WHERE '+contains_query+' ORDER BY len(description) ASC'
        logging.warning(query)
        cursor.execute(query)
        results = cursor.fetchall()
    if results is None or results == []:   #Handles user input ingredient having too many, incorrectly spelled, or non-existent components by removing them until results are found
        i = 1
        j = 0
        for element in component_list:
            if element[-1] == 's':
                component_list[j] = element[0:-1]
            j = j+1
        possible_combinations = list(itertools.combinations(component_list,len(component_list)-i))
        logging.warning("combinations input = "+str(component_list))
        while (results is None or results == []) and i<len(possible_combinations):     #TODO: Change to breadth first rather than depth first. EX "pork" "cheeks" "cleaned" goes to "cleaned" to "cleaned shrimp", should go to "pork" "cheek" first
            logging.warning(possible_combinations[i])
            
            if len(list(possible_combinations[i])) >1:
                results = get_matching_ingredients_from_database(' '.join(list(possible_combinations[i])))
            else: 
                results = get_matching_ingredients_from_database(list(possible_combinations[i])[0])
            i = i+1
            possible_combinations = list(itertools.combinations(component_list,len(component_list)-i))
    if results is None or results == []:
        raise NoSuchEntryError(ingredient)
    return results

#gets the conversion factor tuple (convertable calories per gram of protein,fat,carbs)
def calorie_conversion_factor(ingredient_fdc_id):     
    with connection.cursor() as cursor:
        logging.warning("ID == "+ingredient_fdc_id)
        cursor.execute('SELECT id FROM dbo.food_nutrient_conversion_factor WHERE fdc_id = %s',(ingredient_fdc_id,))
        nutrient_conversion_factor_id = cursor.fetchone()
        logging.warning("get protein,fat,carb where conversion == %s",nutrient_conversion_factor_id)
        if not nutrient_conversion_factor_id is None:
            cursor.execute('SELECT protein_value, fat_value, carbohydrate_value FROM dbo.food_calorie_conversion_factor WHERE food_nutrient_conversion_factor_id = %s',nutrient_conversion_factor_id)
            conversion_factors = cursor.fetchone()
        else:
            conversion_factors = (4,9,4)
        logging.warning(conversion_factors)
    return conversion_factors

def nutrient_gram_amounts(ingredient_fdc_id):  #nutriend id EITHER = 1003,1004,1005 OR 203,204,205
    with connection.cursor() as cursor:
        logging.warning("get food nutrient where ID == "+ingredient_fdc_id)
        cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 1003',(ingredient_fdc_id,))  #protein = 1003, fat = 1004, carbohydrate = 1005
        nutrient_amounts = list() 
        nutrient_amounts.append(cursor.fetchone())
        cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 1004',(ingredient_fdc_id,))
        nutrient_amounts.append(cursor.fetchone())
        cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 1005',(ingredient_fdc_id,))
        nutrient_amounts.append(cursor.fetchone())
        logging.warning("List of nutrient amounts (protein, fat, carbs)(1003,1004,1005):"+nutrient_amounts.__str__())
        if(nutrient_amounts[0] is None):
            nutrient_amounts = []
            cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 203',(ingredient_fdc_id,))  #protein = 1003, fat = 1004, carbohydrate = 1005 
            nutrient_amounts.append(cursor.fetchone())
            cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 204',(ingredient_fdc_id,))
            nutrient_amounts.append(cursor.fetchone())
            cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 205',(ingredient_fdc_id,))
            nutrient_amounts.append(cursor.fetchone())
        logging.warning("List of nutrient amounts (protein,fat,carbs)(203,204,205):"+nutrient_amounts.__str__())

    return nutrient_amounts

def CalculateCalories(ingredient_fdc_id, mass) ->int:
    conversion_factors = calorie_conversion_factor(ingredient_fdc_id) #convertable kcal per gram
    protein_factor = float(conversion_factors[0])
    fat_factor =  float(conversion_factors[1])
    carbs_factor =  float(conversion_factors[2])

    nutrient_amounts = nutrient_gram_amounts(ingredient_fdc_id)
    protein_grams = float(nutrient_amounts[0][0])
    fat_grams = float(nutrient_amounts[1][0])
    carbs_grams = float(nutrient_amounts[2][0])
    total_kCal = protein_factor*protein_grams + fat_factor * fat_grams + carbs_factor * carbs_grams
    total_kCal = total_kCal * (mass/100.0)

    return int(round(total_kCal))
