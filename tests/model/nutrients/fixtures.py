from typing import Dict, List
from unittest import mock

import model
# Import test configs to allow us to build the test globals;
from . import test_configs

# Validate the test flag configs;
model.nutrients.validation.validate_configs(test_configs)

PRIMARY_AND_ALIAS_NUTRIENT_NAMES: List[str]
NUTRIENT_GROUP_NAMES: List[str]
OPTIONAL_NUTRIENT_NAMES: List[str]
GLOBAL_NUTRIENTS: Dict[str, 'model.nutrients.Nutrient']
# Patch to the test configs while we build these;
# with mock.patch('model.nutrients.nutrient.configs', test_configs):
NUTRIENT_GROUP_NAMES = model.nutrients.build_nutrient_group_name_list(test_configs)
OPTIONAL_NUTRIENT_NAMES = model.nutrients.build_optional_nutrient_name_list(test_configs)
PRIMARY_AND_ALIAS_NUTRIENT_NAMES = model.nutrients.build_primary_and_alias_nutrient_names(test_configs)
GLOBAL_NUTRIENTS = model.nutrients.build_global_nutrient_list(test_configs)


def use_test_nutrients(func):
    @mock.patch('model.nutrients.GLOBAL_NUTRIENTS', GLOBAL_NUTRIENTS)
    @mock.patch('model.nutrients.NUTRIENT_GROUP_NAMES', NUTRIENT_GROUP_NAMES)
    @mock.patch('model.nutrients.OPTIONAL_NUTRIENT_NAMES', OPTIONAL_NUTRIENT_NAMES)
    @mock.patch('model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES', PRIMARY_AND_ALIAS_NUTRIENT_NAMES)
    @mock.patch('model.nutrients.configs', test_configs)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def get_protein() -> 'model.nutrients.Nutrient':
    return model.nutrients.GLOBAL_NUTRIENTS['protein']


def get_vitamin_b12() -> 'model.nutrients.Nutrient':
    return model.nutrients.GLOBAL_NUTRIENTS['cobalamin']


def get_undefined_protein_mass() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient=get_protein(),
        get_quantity_in_g=lambda: None,
        get_quantity_pref_unit='g'
    )


def get_32g_protein() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient=get_protein(),
        get_quantity_in_g=lambda: 32,
        get_quantity_pref_unit='g'
    )


def get_undefined_settable_protein_mass() -> 'model.nutrients.SettableNutrientMass':
    return model.nutrients.SettableNutrientMass(nutrient_name="protein")
