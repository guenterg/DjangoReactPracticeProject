from rest_framework import serializers
from .models import DetailedRecipe, Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id','title','description')

class DetailedRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailedRecipe
        fields = ('id', 'origin_id', 'ingredients_list','calories')