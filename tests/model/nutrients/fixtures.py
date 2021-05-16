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


def get_10g_tirbur() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient_name="tirbur",
        quantity_data_src=lambda: model.quantity.QuantityData(
            quantity_in_g=10,
            pref_unit='g'
        )
    )


def get_100mg_docbe() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient_name="docbe",
        quantity_data_src=lambda: model.quantity.QuantityData(
            quantity_in_g=0.1,
            pref_unit='mg'
        )
    )


def get_undefined_docbe() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient_name="docbe",
        quantity_data_src=lambda: model.quantity.QuantityData(
            quantity_in_g=None,
            pref_unit='g'
        )
    )


def get_settable_nutrient_mass(nutrient_name: str) -> model.nutrients.SettableNutrientMass:
    return model.nutrients.SettableNutrientMass(
        nutrient_name=nutrient_name,
        quantity_data=model.quantity.QuantityData(
            quantity_in_g=1.2,
            pref_unit="mg"
        )
    )
