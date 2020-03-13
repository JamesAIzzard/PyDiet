from typing import Dict, TYPE_CHECKING
import json
import pydiet.configs as configs
from pydiet.ingredients.ingredient import Ingredient
if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient

SUMMARY_TEMPLATE = '''Ingredient Summary
--------------------------------
Name: {name}
Cost:
    £{cost}/{cost_mass}{cost_mass_units}
Flags:
    Nut Free: {nut_free}
    Gluten Free: {gluten_free}
    Dairy Free: {dairy_free}
    Alchohol Free: {alchohol_free}
    Caffiene Free: {caffiene_free}
    Vegetarian: {vegetarian}
    Vegan: {vegan}
Macronutrient Totals:
    Total Carbohydrate: {tc_mass}{tc_mass_units}/{tc_mass_per}{tc_mass_per_units} ({tc_perc}%)
    Total Fat: {tf_mass}{tf_mass_units}/{tf_mass_per}{tf_mass_per_units} ({tf_perc}%)
'''

class IngredientService():
    def __init__(self):
        self.current_data: Dict
        self.current_ingredient: 'Ingredient'

    @staticmethod
    def get_data_template() -> dict:
        '''Returns an ingredient data dictionary object.

        Returns:
            dict: A dictionary, the blank data template.
        '''
        # Read the template contents;
        with open(configs.INGREDIENT_DATAFILE_TEMPLATE_PATH) as fh:
            template_data = fh.read()
            # Parse into dict;
            template_dict = json.loads(template_data)
            return template_dict

    @staticmethod
    def summarise(ingredient: 'Ingredient') -> str:
            return SUMMARY_TEMPLATE.format(
                cost=ingredient.cost_data['cost'],
                cost_mass=ingredient.cost_data['mass'],
                cost_mass_units=ingredient.cost_data['cost_mass_units'],
                nut_free=ingredient.get_flag('nut_free'),
                gluten_free=ingredient.get_flag('gluten_free'),
                dairy_free=ingredient.get_flag('dairy_free'),
                alchohol_free=ingredient.get_flag('alchohol_free'),
                caffiene_free=ingredient.get_flag('caffiene_free'),
                vegetarian=ingredient.get_flag('vegetarian'),
                vegan=ingredient.get_flag('vegan'),
                tc_mass=ingredient.total_carbohydrate_data['mass'],
                tc_mass_units=ingredient.total_carbohydrate_data['mass_units'],
                tc_mass_per=ingredient.total_carbohydrate_data['mass_per'],
                tc_mass_per_units=ingredient.total_carbohydrate_data['mass_per_units'],
                tc_perc=ingredient.total_carbohydrate_percentage,
                tf_mass=ingredient.total_fat_data['mass'],
                tf_mass_units=ingredient.total_fat_data['mass_units'],
                tf_mass_per=ingredient.total_fat_data['mass_per'],
                tf_mass_per_units=ingredient.total_fat_data['mass_per_units'],
                tf_perc=ingredient.total_fat_percentage                
            )

ingredient_service = IngredientService()