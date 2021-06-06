"""Tests for the HasNutrientRatios base class."""
from typing import Dict, List, Optional, Any
from unittest import mock

import model
# Import test configs to allow us to build the test globals;
from . import test_configs
from tests.model.quantity import fixtures as qfx

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


class NutrientRatioBaseTestable(model.nutrients.NutrientRatioBase):
    """A minimal implementation of BaseNutrientRatio to allow its testing."""

    def __init__(
            self,
            nutrient_name:str,
            ratio_host: Any,
            quantity_ratio_data: 'model.quantity.QuantityRatioData',
    ):
        """
        Args:
            nutrient_name (str):
            ratio_host (Any):
            quantity_ratio_data (model.quantity.QuantityRatioData):
        """
        super().__init__(nutrient_name=nutrient_name, ratio_host=ratio_host)
        self._quantity_ratio_data = quantity_ratio_data

    @property
    def quantity_ratio_data(self) -> 'model.quantity.QuantityRatioData':
        """Returns quantity ratio data."""
        return self._quantity_ratio_data


class HasReadableNutrientRatiosTestable(model.nutrients.HasReadableNutrientRatios):
    """Minimal class to allow testing of the HasNutrientRatios abstract base class."""

    def __init__(self, nutrient_ratios_data: 'model.nutrients.NutrientRatiosData' = None, **kwargs):
        super().__init__(**kwargs)

        # If no data was provided, init an empty dict;
        if nutrient_ratios_data is None:
            self._nutrient_ratios_data_: 'model.nutrients.NutrientRatiosData' = {}
        # Otherwise go ahead and load the data;
        else:
            self._nutrient_ratios_data_ = nutrient_ratios_data

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratios for the instance;"""
        return self._nutrient_ratios_data_


class HasNutrientRatiosAndExtUnitsTestable(
    HasReadableNutrientRatiosTestable,
    qfx.HasReadableExtendedUnitsTestable
):
    """Minimal implementation to allow testing of HasNutrientRatios in conjunction with SupportsExtendedUnits."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class HasSettableNutrientRatiosAndExtUnitsTestable(
    model.nutrients.HasSettableNutrientRatios,
    model.quantity.HasReadableExtendedUnits
):
    """Minimal class to allow testing of the HasSettableNutrientRatios while also supporting extended units."""

    def __init__(self, g_per_ml: Optional[float] = None, piece_mass_g: Optional[float] = None):  # noqa
        super().__init__()
        self._g_per_ml_: Optional[float] = g_per_ml
        self._piece_mass_g_: Optional[float] = piece_mass_g

    @property
    def _g_per_ml(self) -> Optional[float]:
        return self._g_per_ml_

    @property
    def _piece_mass_g(self) -> Optional[float]:
        return self._piece_mass_g_


class HasReadableNutrientMassesTestable(model.nutrients.HasReadableNutrientMasses, model.quantity.IsSettableQuantityOf):
    """Minimal implementation for testing HasNutrientMasses."""


def use_test_nutrients(func):
    """Decorator to apply all patches required to use the test nutrients."""

    @mock.patch('model.nutrients.GLOBAL_NUTRIENTS', GLOBAL_NUTRIENTS)
    @mock.patch('model.nutrients.NUTRIENT_GROUP_NAMES', NUTRIENT_GROUP_NAMES)
    @mock.patch('model.nutrients.OPTIONAL_NUTRIENT_NAMES', OPTIONAL_NUTRIENT_NAMES)
    @mock.patch('model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES', PRIMARY_AND_ALIAS_NUTRIENT_NAMES)
    @mock.patch('model.nutrients.configs', test_configs)
    def wrapper(*args, **kwargs):
        """Wrapper function for the decorator to return."""
        return func(*args, **kwargs)

    return wrapper
