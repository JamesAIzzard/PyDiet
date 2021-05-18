from typing import Dict, List, Callable, Optional, Any
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


class HasNutrientRatiosTestable(model.nutrients.HasNutrientRatios):
    def __init__(self):
        self._nutrient_ratios: Dict[str, 'model.nutrients.NutrientRatio'] = {}

    @property
    def nutrient_ratios(self) -> Dict[str, 'model.nutrients.NutrientRatio']:
        return self._nutrient_ratios


class HasSettableNutrientRatiosAndDensityTestable(
    model.nutrients.HasSettableNutrientRatios,
    model.quantity.SupportsExtendedUnits
):
    def __init__(self, g_per_ml: Optional[float] = None, piece_mass_g: Optional[float] = None): # noqa
        super().__init__()
        self._g_per_ml_: Optional[float] = g_per_ml
        self._piece_mass_g_: Optional[float] = piece_mass_g

    @property
    def _g_per_ml(self) -> Optional[float]:
        return self._g_per_ml_

    @property
    def _piece_mass_g(self) -> Optional[float]:
        return self._piece_mass_g_


def use_test_nutrients(func):
    @mock.patch('model.nutrients.GLOBAL_NUTRIENTS', GLOBAL_NUTRIENTS)
    @mock.patch('model.nutrients.NUTRIENT_GROUP_NAMES', NUTRIENT_GROUP_NAMES)
    @mock.patch('model.nutrients.OPTIONAL_NUTRIENT_NAMES', OPTIONAL_NUTRIENT_NAMES)
    @mock.patch('model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES', PRIMARY_AND_ALIAS_NUTRIENT_NAMES)
    @mock.patch('model.nutrients.configs', test_configs)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def init_10g_tirbur() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient_name="tirbur",
        quantity_data_src=lambda: model.quantity.QuantityData(
            quantity_in_g=10,
            pref_unit='g'
        )
    )


def init_100mg_docbe() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient_name="docbe",
        quantity_data_src=lambda: model.quantity.QuantityData(
            quantity_in_g=0.1,
            pref_unit='mg'
        )
    )


def init_undefined_docbe() -> 'model.nutrients.NutrientMass':
    return model.nutrients.NutrientMass(
        nutrient_name="docbe",
        quantity_data_src=lambda: model.quantity.QuantityData(
            quantity_in_g=None,
            pref_unit='g'
        )
    )


def init_settable_nutrient_mass(nutrient_name: str) -> model.nutrients.SettableNutrientMass:
    return model.nutrients.SettableNutrientMass(
        nutrient_name=nutrient_name,
        quantity_data=model.quantity.QuantityData(
            quantity_in_g=1.2,
            pref_unit="mg"
        )
    )


def init_nutrient_ratio(subject: Any, nutrient_name: str, data_src: Callable) -> 'model.nutrients.NutrientRatio':
    return model.nutrients.NutrientRatio(subject, nutrient_name, data_src)


def init_nutrient_ratio_data(
        nutrient_qty_g: Optional[float] = None,
        nutrient_pref_unit: str = 'g',
        subject_qty_g: Optional[float] = None,
        subject_pref_unit: str = 'g'
):
    """Returns a nutrient ratio data instance, providing default values."""
    return model.nutrients.NutrientRatioData(
        nutrient_mass_data=model.quantity.QuantityData(
            quantity_in_g=nutrient_qty_g,
            pref_unit=nutrient_pref_unit
        ),
        subject_ref_qty_data=model.quantity.QuantityData(
            quantity_in_g=subject_qty_g,
            pref_unit=subject_pref_unit
        )
    )


def init_nutrient_ratio_data_src(
        nutrient_qty_g: Optional[float] = None,
        nutrient_pref_unit: str = 'g',
        subject_qty_g: Optional[float] = None,
        subject_pref_unit: str = 'g'
):
    return lambda: init_nutrient_ratio_data(nutrient_qty_g, nutrient_pref_unit, subject_qty_g, subject_pref_unit)
