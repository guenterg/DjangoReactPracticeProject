from django.contrib import admin
from .models import DetailedRecipe, Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title','description')

class DetailedRecipeAdmin(admin.ModelAdmin):
    list_display = ("origin_id",)
# Register your models here.
admin.site.register(Recipe,RecipeAdmin)
admin.site.register(DetailedRecipe,DetailedRecipeAdmin)