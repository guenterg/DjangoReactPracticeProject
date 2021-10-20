import logging
from typing import cast
from django.db import models
from django.db.models.base import Model
from django.db.models.fields import FloatField, PositiveBigIntegerField

# Create your models here.
class Recipe(models.Model):
    id = models
    title = models.CharField(max_length = 120)
    description = models.TextField()
    def __str__(self) -> str:
        return self.title
    def save(self, *args, **kwargs):
        saved_recipe = super().save(*args, **kwargs)
        ##detail_args = dict(kwargs)
        ##detail_args['description'] = self.description
        ##detail_args['origin_id'] = self
        DetailedRecipe().save( desc = self.description, origin = self)
        return saved_recipe


class DetailedRecipe(models.Model):
    origin_id = models.OneToOneField(Recipe, on_delete=models.CASCADE,primary_key= True, default=-1)
    ingredients_list = models.TextField()
    calories = models.IntegerField(default=0)


    def __str__(self) -> str:
        return self.ingredients_list

    def save(self, desc,origin, *args, **kwargs):
        ##logging.warning(args[0])
        logging.warning(desc)
        self.origin_id = origin
        self.ingredients_list = desc
        self.calories = 100
        saved_recipe = super().save(force_insert= True)


        return saved_recipe
