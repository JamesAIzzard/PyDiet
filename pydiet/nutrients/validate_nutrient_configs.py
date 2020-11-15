import pydiet
from pydiet import nutrients, flags

apnn = nutrients.configs.all_primary_nutrient_names

# Check there are no duplications on all_primary_nutrient_names;
if not len(apnn) == len(set(apnn)):
    raise nutrients.exceptions.NutrientConfigsError('Duplicates exist in the all_primary_nutrient_names list.')

# Check that nutrient_aliases.keys() are in all_primary_nutrient_names;
for name in nutrients.configs.nutrient_aliases.keys():
    if name not in apnn:
        raise nutrients.exceptions.NutrientConfigsError(
            '{} is in nutrient_aliases.keys() but is not a primary nutrient name'.format(name))
# Check that no nutrient_aliases.values() are also in primary_nutrient_names;
for alias_list in nutrients.configs.nutrient_aliases.values():
    for name in alias_list:
        if name in apnn:
            raise nutrients.exceptions.NutrientConfigsError(
                '{} is listed as an alias but is also a primary nutrient name'.format(name))

        # Check that nutrient_group_definitions.keys() are in all_primary_nutrient_names;
for name in nutrients.configs.nutrient_group_definitions.keys():
    if name not in apnn:
        raise nutrients.exceptions.NutrientConfigsError(
            '{} is a group definition key, but is not a primary nutrient name'.format(name))
# Check that nutrient_group_definitions.values() are in all_primary_nutrient_names;
for group_name in nutrients.configs.nutrient_group_definitions.keys():
    for name in nutrients.configs.nutrient_group_definitions[group_name]:
        if name not in apnn:
            raise nutrients.exceptions.NutrientConfigsError(
                '{} is in included in the group {} but is not a primary nutrient name'.format(name, group_name))

# Check that nutrient_flag_rels.keys() are in all_flag_names;
for flag_name in pydiet.configs.flag_nutrient_relations:
    if flag_name not in flags.configs.all_flag_names:
        raise nutrients.exceptions.NutrientConfigsError(
            '{} is in nutrient_flag_rels but not in all_flag_names'.format(flag_name))

# Check that nutrient_flag_rels.values() are in all_primary_nutrient_names;
for flag_name in pydiet.configs.flag_nutrient_relations:
    for name in pydiet.configs.flag_nutrient_relations[flag_name]:
        if name not in apnn:
            raise nutrients.exceptions.NutrientConfigsError(
                '{} is in nutrient_flag_rels but is not a primary nutrient name'.format(name))

# Check that all calorie_nutrients.keys() are in all_primary_nutrient_names;
for name in nutrients.configs.calorie_nutrients.keys():
    if name not in apnn:
        raise nutrients.exceptions.NutrientConfigsError(
            '{} is in calorie_nutrients.keys() but is not a primary nutrient name'.format(name))
