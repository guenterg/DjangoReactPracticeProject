from typing import Tuple
from django.db import models
from models import DetailedRecipe
import inspect
import difflib

def total_value(name:str, weight:float):
    return -1

def greatest_second_value(matches:"list[Tuple[str,float]]"):
    max_ratio = max(matches,key=lambda k:matches[k])
    return max_ratio

def closest_str(name:str) -> str:
    results = 0 ##get sql results here  nutritionvalues.dbo.food column 'description' for name (ex. 'Onions, raw')
    matcher = difflib.SequenceMatcher()
    matches = []
    i = 0
    for res in results:
        matcher.set_seq1(name)
        matcher.set_seq2(res)
        matches[i] = (res, matcher.quick_ratio())
        i = i+1

    closest_match = greatest_second_value(matches)
    return closest_match