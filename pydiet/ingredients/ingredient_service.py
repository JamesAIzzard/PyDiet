from typing import TYPE_CHECKING
import json

from pinjector import inject

from pydiet.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from pydiet.ingredients.ingredient import Ingredient, NutrientAmount
    from pydiet.utility_service import UtilityService
    from pydiet.data import repository_service
    from pydiet import configs


def resolve_alias(alias: str) -> str:
    configs: 'configs' = inject('pydiet.configs')
    # Hunt through the alias list and return rootname
    # if match is found;
    for rootname in configs.NUTRIENT_ALIASES.keys():
        if alias in configs.NUTRIENT_ALIASES[rootname]:
            return rootname
    # Not found, just return;
    return alias


def get_new_ingredient() -> Ingredient:
    rs: 'repository_service' = inject('pydiet.repository_service')
    data_template = rs.read_ingredient_data_template()
    return Ingredient(data_template)

# INGREDIENT_SUMMARY_TEMPLATE = '''Name:
# # {name}

# # --------------------------------------
# # Cost:
# # {cost}

# # --------------------------------------
# # Flags:
# # {flags}

# # --------------------------------------
# # Primary Nutrients:
# # {primary_nutrients}
# # '''

# INGREDIENT_COST_SUMMARY_TEMPLATE = '£{cost:.2f} for {mass}{mass_units} (£{g_cost:.3f}/g)'
# INGREDIENT_FLAG_SUMMARY_TEMPLATE = '{flag_name}: {status}'
# NUTRIENT_SUMMARY_TEMPLATE = \
#     '{nutrient_name}: {nutrient_mass}{nutrient_mass_units}/{ingredient_mass}{ingredient_mass_units} ({perc:.3f}%)'


# def summarise_ingredient_name(ingredient: Ingredient) -> str:
#     if ingredient.name:
#         return ingredient.name
#     else:
#         return 'Undefined'

# def summarise_ingredient_cost(ingredient: Ingredient) -> str:
#     if ingredient.cost_is_defined:
#         cost_data = ingredient.cost_data
#         return INGREDIENT_COST_SUMMARY_TEMPLATE.format(
#             cost=cost_data['cost'],
#             mass=cost_data['ingredient_mass'],
#             mass_units=cost_data['ingredient_mass_units'],
#             g_cost=ingredient.cost_per_g
#         )
#     else:
#         return 'Undefined'

# def summarise_ingredient_flags(ingredient: Ingredient) -> str:
#     utility_service:'UtilityService' = inject('pydiet.utility_service')
#     flag_summary = ''
#     flag_data = ingredient.all_flag_data
#     for flag_name in flag_data.keys():
#         s_flag_name = utility_service.sentence_case(
#             flag_name)
#         if not flag_data[flag_name] == None:
#             status = flag_data[flag_name]
#         else:
#             status = 'Undefined'
#         flag_summary = flag_summary+INGREDIENT_FLAG_SUMMARY_TEMPLATE.format(
#             flag_name=s_flag_name,
#             status=status
#         )+('\n')
#     return flag_summary

# def summarise_nutrient_amount(nutrient_amount:'NutrientAmount')->str:
#     return NUTRIENT_SUMMARY_TEMPLATE.format(
#         nutrient_amount.name,
#         nutrient_amount.nutrient_mass,
#         nutrient_amount.nutrient_mass_units,
#         nutrient_amount.ingredient_mass,
#         nutrient_amount.ingredient_mass_units,
#         nutrient_amount.percentage
#     )

# def summarise_ingredient(ingredient: Ingredient) -> str:
#     return INGREDIENT_SUMMARY_TEMPLATE.format(
#         name=summarise_ingredient_name(ingredient),
#         cost=summarise_ingredient_cost(ingredient),
#         flags=summarise_ingredient_flags(ingredient),
#     )

