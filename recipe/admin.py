from django.contrib import admin
import logging
from .models import DetailedRecipe, DetailedRecipeCalorieContributions, Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title','description')

class DetailedRecipeAdmin(admin.ModelAdmin):
    list_display = ("origin_id",)



class DetailedRecipeCalorieContributionsAdmin(admin.ModelAdmin):
    list_display= ('parent_recipe_id','ingredient','calories')
# Register your models here.
admin.site.register(Recipe,RecipeAdmin)
admin.site.register(DetailedRecipe,DetailedRecipeAdmin)
admin.site.register(DetailedRecipeCalorieContributions,DetailedRecipeCalorieContributionsAdmin)