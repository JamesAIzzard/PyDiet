from typing import Optional, TYPE_CHECKING
import json
import pydiet.configs as configs
from pinjector import inject
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
Macronutrient Totals:
{macro_totals}

--------------------------------------
Macronutrients:
{macros}

--------------------------------------
Micronutrients:
{micros}
'''

INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} ({g_cost}/g)'
INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'
NUTRIENT_SUMMARY_TEMPLATE = \
    '{nutrient_name}: {mass}{mass_units}/{mass_per}{mass_per_units} ({perc}%)'


class IngredientService():
    def __init__(self):
        self._utility_service: UtilityService = inject('utility_service')

    @staticmethod
    def _get_data_template() -> dict:
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
    def summarise_ingredient_name(ingredient: Ingredient) -> str:
        if ingredient.name:
            return ingredient.name
        else:
            return 'Undefined'

    @staticmethod
    def summarise_ingredient_cost(ingredient: Ingredient) -> str:
        if ingredient.cost_is_defined:
            cost_data = ingredient.cost_data
            return INGREDIENT_COST_SUMMARY_TEMPLATE.format(
                cost=cost_data['cost'],
                mass=cost_data['mass'],
                mass_units=cost_data['mass_units'],
                g_cost=ingredient.cost_per_g
            )
        else:
            return 'Undefined'

    def summarise_ingredient_flags(self, ingredient: Ingredient) -> str:
        flag_summary = ''
        flag_data = ingredient.flag_data
        for flag_name in flag_data.keys():
            s_flag_name = self._utility_service.sentence_case(
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

    def summarise_nutrient(self, nutrient_name: str, ingredient: Ingredient) -> str:
        '''Generates a string summary of the nutrient. Inserts word 'undefined'
        if any of the nutrient's fields are undefined.

        Args:
            nutrient_name (str): Name of nutrient to summarise.
            ingredient (Ingredient): Ingredient which the nutrient belongs to.

        Returns:
            str: Text summary of the nutrient.
        '''
        s_nutrient_name = self._utility_service.sentence_case(nutrient_name)
        if ingredient.check_nutrient_is_defined(nutrient_name):
            nutrient_data = ingredient.get_nutrient_data(nutrient_name)
            return NUTRIENT_SUMMARY_TEMPLATE.format(
                nutrient_name=self._utility_service.sentence_case(
                    nutrient_name),
                mass=nutrient_data['mass'],
                mass_units=nutrient_data['mass_units'],
                mass_per=nutrient_data['mass_per'],
                mass_per_units=nutrient_data['mass_per_units'],
                perc=ingredient.get_nutrient_percentage(s_nutrient_name)
            )
        else:
            return '{}: Undefined'.format(s_nutrient_name)

    def summarise_macro_totals(self, ingredient: Ingredient) -> str:
        macro_totals_summary = ''
        for macro_total_name in ingredient.macronutrient_totals_data.keys():
            macro_totals_summary = macro_totals_summary +\
                self.summarise_nutrient(macro_total_name, ingredient)+'\n'
        return macro_totals_summary

    def summarise_macros(self, ingredient: Ingredient) -> str:
        macros_summary = ''
        for macro_name in ingredient.macronutrient_data.keys():
            macros_summary = macros_summary +\
                self.summarise_nutrient(macro_name, ingredient) + '\n'
        return macros_summary

    def summarise_micros(self, ingredient: Ingredient) -> str:
        micros_summary = ''
        for micro_name in ingredient.micronutrient_data.keys():
            micros_summary = micros_summary +\
                self.summarise_nutrient(micro_name, ingredient) + '\n'
        return micros_summary

    def summarise_ingredient(self, ingredient: Ingredient) -> str:
        return INGREDIENT_SUMMARY_TEMPLATE.format(
            name=IngredientService.summarise_ingredient_name(ingredient),
            cost=IngredientService.summarise_ingredient_cost(ingredient),
            flags=self.summarise_ingredient_flags(ingredient),
            macro_totals=self.summarise_macro_totals(ingredient),
            macros=self.summarise_macros(ingredient),
            micros=self.summarise_micros(ingredient)
        )

    @staticmethod
    def get_new_ingredient() -> Ingredient:
        data_template = IngredientService._get_data_template()
        return Ingredient(data_template)
