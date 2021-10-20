from django.http.response import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

import recipe
from .serializers import RecipeSerializer, DetailedRecipeSerializer
from .models import DetailedRecipe, Recipe


# Create your views here.

class RecipeView(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

class DetailedRecipeView(RecipeView):
    serializer_class = DetailedRecipeSerializer
    queryset = DetailedRecipe.objects.all()


