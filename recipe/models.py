import logging
from django.db import connection
from typing import cast
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import FloatField, PositiveBigIntegerField
#from matching import closest_str

# Create your models here.
class Recipe(models.Model):
    id = models
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


        ingredient = single_ingredient(self.ingredients_list, 0)
        fdc_id = 170000 #closest_str(ingredient)


        self.calories = CalculateCalories(str(fdc_id))
        saved_recipe = super().save(force_insert= True)
        return saved_recipe

def single_ingredient(ingredient_list, index) -> str:
    return ""

#gets the conversion factor tuple (convertable calories per gram of protein,fat,carbs)
def calorie_conversion_factor(ingredient_fdc_id):     
    with connection.cursor() as cursor:
        cursor.execute('SELECT id FROM dbo.food_nutrient_conversion_factor WHERE fdc_id = %s',(ingredient_fdc_id,))
        nutrient_conversion_factor_id = cursor.fetchone()
        cursor.execute('SELECT protein_value, fat_value, carbohydrate_value FROM dbo.food_calorie_conversion_factor WHERE food_nutrient_conversion_factor_id = %s',nutrient_conversion_factor_id)
        conversion_factors = cursor.fetchone()
        logging.warning(conversion_factors)
    return conversion_factors

def nutrient_gram_amounts(ingredient_fdc_id):
    with connection.cursor() as cursor:
        cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 1003',(ingredient_fdc_id,))  #protein = 1003, fat = 1004, carbohydrate = 1005
        nutrient_amounts = list() 
        nutrient_amounts.append(cursor.fetchone())
        cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 1004',(ingredient_fdc_id,))
        nutrient_amounts.append(cursor.fetchone())
        cursor.execute('SELECT amount FROM dbo.food_nutrient WHERE fdc_id = %s AND nutrient_id = 1005',(ingredient_fdc_id,))
        nutrient_amounts.append(cursor.fetchone())
    return nutrient_amounts

def CalculateCalories(ingredient_fdc_id) ->int:
    conversion_factors = calorie_conversion_factor(ingredient_fdc_id) #convertable kcal per gram
    protein_factor = float(conversion_factors[0])
    fat_factor =  float(conversion_factors[1])
    carbs_factor =  float(conversion_factors[2])

    nutrient_amounts = nutrient_gram_amounts(ingredient_fdc_id)
    protein_grams = float(nutrient_amounts[0][0])
    fat_grams = float(nutrient_amounts[1][0])
    carbs_grams = float(nutrient_amounts[2][0])
    total_kCal = protein_factor*protein_grams + fat_factor * fat_grams + carbs_factor * carbs_grams


    return int(round(total_kCal))
