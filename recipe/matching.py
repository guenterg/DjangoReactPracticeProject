from typing import Tuple
import inspect
import difflib

common_terms = ("cooked","raw","boiled","salt","skin","peel","steamed","poached","smoked","baked","broiled","made","with","flesh","NFS","from","fresh","peel","made","with" )

def total_value(name:str, weight:float):
    return -1

def greatest_second_value(matches:"list[Tuple[str,float]]"):

    max_ratio = max(matches,key=lambda k:k[1])
    return max_ratio[0]

def closest_str(name:str, ingredient_results:list(tuple())):

    return closest_str_helper(name, ingredient_results)


def closest_str_helper(name:str, results:list(tuple())) -> str:
    #sort elements alphabetically for best matching
    matcher = difflib.SequenceMatcher()
    matches = []
    name = name.lower()
    for (res, id) in results:
        pruned = remove_common_terms(res).lower()
        matcher.set_seq1(name)
        matcher.set_seq2(pruned)
        matches.append((res, matcher.quick_ratio()))
    closest_match = greatest_second_value(matches)
    return closest_match


#remove common terms in raw and cooked ingredient descriptions, replacing them with # for purposes of match comparison. Remove commas and spaces.
def remove_common_terms(description:str):
    pruned = str(description)
    for term in common_terms:
        pruned = pruned.replace(term, '#')
    pruned = pruned.replace(',', '')
    pruned = pruned.replace(' ','')
    return pruned