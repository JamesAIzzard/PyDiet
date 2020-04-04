from typing import TYPE_CHECKING
import json

from pinjector import inject

import pydiet.configs as configs
from pydiet.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient
    from pydiet.utility_service import UtilityService

INGREDIENT_SUMMARY_TEMPLATE = '''Name:
{name}

--------------------------------------
Cost:
{cost}

--------------------------------------
Flags:
{flags}

--------------------------------------
Primary Nutrients:
{primary_nutrients}

--------------------------------------
All Nutrients:
{all_nutrients}
'''

INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} (£{g_cost:.3f}/g)'
INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'
NUTRIENT_SUMMARY_TEMPLATE = \
    '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_mass}{ingredient_mass_units} ({perc:.3f}%)'

def summarise_ingredient_name(ingredient: Ingredient) -> str:
    if ingredient.name:
        return ingredient.name
    else:
        return 'Undefined'

def summarise_ingredient_cost(ingredient: Ingredient) -> str:
    if ingredient.cost_is_defined:
        cost_data = ingredient.cost_data
        return INGREDIENT_COST_SUMMARY_TEMPLATE.format(
            cost=cost_data['cost'],
            mass=cost_data['ingredient_mass'],
            mass_units=cost_data['ingredient_mass_units'],
            g_cost=ingredient.cost_per_g
        )
    else:
        return 'Undefined'

def summarise_ingredient_flags(ingredient: Ingredient) -> str:
    utility_service:'UtilityService' = inject('pydiet.utility_service')
    flag_summary = ''
    flag_data = ingredient.flag_data
    for flag_name in flag_data.keys():
        s_flag_name = utility_service.sentence_case(
            flag_name)
        if not flag_data[flag_name] == None:
            status = flag_data[flag_name]
        else:
            status = 'Undefined'
        flag_summary = flag_summary+INGREDIENT_FLAG_SUMMARY_TEMPLATE.format(
            flag_name=s_flag_name,
            status=status
        )+('\n')
    return flag_summary

# TODO - Replace these with summarise group and summarise molecule

def summarise_nutrient(ingredient:'Ingredient', nutrient_name:str)->str:
    # First, resolve nutrient against alias if required;


def summarise_molecule(ingredient: 'Ingredient', molecule_name:str):
    check_molecule_name(molecule_name)
    _summarise_component(ingredient.get_molecule_data[molecule_name], molecule_name)

def summarise_group(ingredient: 'Ingredient', group_name:str):
    check_group_name(group_name)
    _summarise_component(ingredient.get_group_data[group_name], group_name)

# def summarise_nutrient(self, nutrient_name: str, ingredient: Ingredient) -> str:
#     '''Generates a string summary of the nutrient. Inserts word 'undefined'
#     if any of the nutrient's fields are undefined.

#     Args:
#         nutrient_name (str): Name of nutrient to summarise.
#         ingredient (Ingredient): Ingredient which the nutrient belongs to.

#     Returns:
#         str: Text summary of the nutrient.
#     '''
#     s_nutrient_name = self._utility_service.sentence_case(nutrient_name)
#     if ingredient.check_nutrient_is_defined(nutrient_name):
#         nutrient_data = ingredient.get_nutrient_data(nutrient_name)
#         return NUTRIENT_SUMMARY_TEMPLATE.format(
#             nutrient_name=self._utility_service.sentence_case(
#                 nutrient_name),
#             mass=nutrient_data['mass'],
#             mass_units=nutrient_data['mass_units'],
#             mass_per=nutrient_data['mass_per'],
#             mass_per_units=nutrient_data['mass_per_units'],
#             perc=ingredient.get_nutrient_percentage(nutrient_name)
#         )
#     else:
#         return '{}: Undefined'.format(s_nutrient_name)

# def summarise_macro_totals(self, ingredient: Ingredient) -> str:
#     macro_totals_summary = ''
#     for macro_total_name in ingredient.macronutrient_totals_data.keys():
#         macro_totals_summary = macro_totals_summary +\
#             self.summarise_nutrient(macro_total_name, ingredient)+'\n'
#     return macro_totals_summary

# def summarise_macros(self, ingredient: Ingredient) -> str:
#     macros_summary = ''
#     for macro_name in ingredient.macronutrient_data.keys():
#         macros_summary = macros_summary +\
#             self.summarise_nutrient(macro_name, ingredient) + '\n'
#     return macros_summary

# def summarise_micros(self, ingredient: Ingredient) -> str:
#     micros_summary = ''
#     for micro_name in ingredient.micronutrient_data.keys():
#         micros_summary = micros_summary +\
#             self.summarise_nutrient(micro_name, ingredient) + '\n'
#     return micros_summary

def summarise_ingredient(ingredient: Ingredient) -> str:
    return INGREDIENT_SUMMARY_TEMPLATE.format(
        name=IngredientService.summarise_ingredient_name(ingredient),
        cost=IngredientService.summarise_ingredient_cost(ingredient),
        flags=self.summarise_ingredient_flags(ingredient),
        macro_totals=self.summarise_macro_totals(ingredient),
        macros=self.summarise_macros(ingredient),
        micros=self.summarise_micros(ingredient)
    )

def get_new_ingredient() -> Ingredient:
    data_template = IngredientService._get_data_template()
    return Ingredient(data_template)
