"""Tests for the HasNutrientRatios base class."""
from typing import Dict, List, Callable, Optional, Any
from unittest import mock

import model
# Import test configs to allow us to build the test globals;
from tests.model.nutrients import test_configs
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


class BaseNutrientRatioTestable(model.nutrients.ReadableNutrientRatio):
    """A minimal implementation of BaseNutrientRatio to allow its testing."""

    def __init__(self, subject: Any,
                 nutrient_name: str,
                 nutrient_ratio_data: 'model.nutrients.NutrientRatioData'):
        # Store nutrient mass and subject ref qty locally for testing;
        self._nutrient_mass = model.nutrients.ReadonlyNutrientMass(
            nutrient_name=nutrient_name,
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(
                qty_in_g=nutrient_ratio_data['nutrient_mass_data']['quantity_in_g'],
                pref_unit=nutrient_ratio_data['nutrient_mass_data']['pref_unit']
            ))
        )
        self._subject_ref_qty = model.quantity.HasReadonlyQuantityOf(
            qty_subject=subject,
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(
                qty_in_g=nutrient_ratio_data['subject_ref_qty_data']['quantity_in_g'],
                pref_unit=nutrient_ratio_data['subject_ref_qty_data']['pref_unit']
            ))
        )

    @property
    def nutrient_mass(self) -> 'model.nutrients.ReadonlyNutrientMass':
        """Return the locally stored instance."""
        return self._nutrient_mass

    @property
    def subject_ref_quantity(self) -> 'model.quantity.HasReadonlyQuantityOf':
        """Return the locally stored ref quantity."""
        return self._subject_ref_qty


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


class HasReadableNutrientMassesTestable(model.nutrients.HasReadableNutrientMasses, model.quantity.HasSettableQuantityOf):
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


def get_nutrient_ratio_data(
        nutrient_mass_g: Optional[float] = None,
        nutrient_mass_unit: str = 'g',
        subject_qty_g: Optional[float] = None,
        subject_qty_unit: str = 'g',
) -> 'model.nutrients.NutrientRatioData':
    """Helper function to create nutrient ratio data. Provides default values when values not specified."""
    return model.nutrients.NutrientRatioData(
        nutrient_mass_data=model.nutrients.NutrientMassData(
            quantity_in_g=nutrient_mass_g,
            pref_unit=nutrient_mass_unit
        ),
        subject_ref_qty_data=model.quantity.QuantityData(
            quantity_in_g=subject_qty_g,
            pref_unit=subject_qty_unit
        )
    )


def get_nutrient_ratio_data_src(nutrient_ratio_data: 'model.nutrients.NutrientRatioData') \
        -> Callable[[None], 'model.nutrients.NutrientRatioData']:
    """Returns a nutrient ratio data source callable."""
    return lambda: nutrient_ratio_data
