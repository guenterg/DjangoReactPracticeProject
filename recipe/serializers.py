from rest_framework import serializers
from .models import DetailedRecipe, Recipe
from django.db import connection

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id','title','description')

class DetailedRecipeSerializer(serializers.ModelSerializer):
    ingredients = serializers.SerializerMethodField()
    class Meta:
        model = DetailedRecipe
        fields = ('id', 'origin_id', 'ingredients_list','calories','ingredients')

    def get_ingredients(self, obj):
        with connection.cursor() as cursor:
            query = "SELECT * FROM dbo.recipe_detailedrecipecaloriecontributions WHERE parent_recipe_id_id = '"+obj+"'"
            cursor.execute(query)
            results = cursor.fetchall()
        return str(results)