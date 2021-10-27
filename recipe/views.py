from django.core.handlers.wsgi import WSGIRequest
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from django.db import connection
import logging


import recipe
from .serializers import RecipeSerializer, DetailedRecipeSerializer
from .models import DetailedRecipe, Recipe, DetailedRecipeCalorieContributions


# Create your views here.

class RecipeView(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

class DetailedRecipeView(viewsets.ReadOnlyModelViewSet):
    serializer_class = DetailedRecipeSerializer
    queryset = DetailedRecipe.objects.all()


def calorie_contribution(recipe:WSGIRequest):
    return HttpResponse(get_ingredients((recipe.path.split('/')[-1])))

def get_ingredients(recipe_id):
        with connection.cursor() as cursor:
            query = "SELECT * FROM dbo.recipe_detailedrecipecaloriecontributions WHERE parent_recipe_id_id = "+recipe_id
            cursor.execute(query)
            results = cursor.fetchall()
        ingredient_dict = {}
        for result  in results:
            ingredient_dict[result[1]] = [result[2],result[3]]
        logging.warning("Out dict = "+str(ingredient_dict))
        ingredients_json = JsonResponse(ingredient_dict, safe= False)
        logging.warning("out Json = "+ str(ingredients_json.content))
        return ingredients_json