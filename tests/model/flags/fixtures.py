"""Fixtures for flag module tests."""
import unittest
from typing import Dict, Optional, List
from unittest import mock

import model
from tests.model.quantity import fixtures as qfx
from tests.model.nutrients import fixtures as nfx
# Import test configs to allow us to build the global test flag list;
from . import test_configs

# Validate the test flag configs (using the test nutrients);
with mock.patch('model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES', nfx.PRIMARY_AND_ALIAS_NUTRIENT_NAMES):
    nfx.use_test_nutrients(model.flags.validation.validate_configs(test_configs))

# Build the global flag list for testing, using the test configs;
with mock.patch('model.flags.flag.configs', test_configs), \
        mock.patch('model.flags.main.configs', test_configs):
    ALL_FLAGS: Dict[str, 'model.flags.Flag'] = model.flags.build_global_flag_list()


# Create a decorator to look after the patching required to run the test flags;
def use_test_flags(func):
    """Decorator to use patch the flags to the test flags."""
    @mock.patch('model.flags.ALL_FLAGS', ALL_FLAGS)
    @mock.patch('model.flags.flag.configs', test_configs)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        func(*args, **kwargs)

    return wrapper


class HasReadableFlagsTestable(model.flags.HasReadableFlags):
    """Minimal concrete implementation of HasFlags."""
    def __init__(self,
                 flag_dofs: Optional[Dict[str, Optional[bool]]] = None,
                 nutrient_ratios_data: Optional['model.nutrients.NutrientRatiosData'] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._flag_dofs_ = flag_dofs if flag_dofs is not None else {}
        self._nutrient_ratios_data_ = nutrient_ratios_data if nutrient_ratios_data is not None else {}

    @property
    def flag_dofs(self) -> 'model.flags.FlagDOFData':
        """Returns flag dofs."""
        return self._flag_dofs_

    @property
    def nutrient_ratios_data(self) -> Dict[str, 'mock.Mock']:
        """Returns nutrient ratios data."""
        return self._nutrient_ratios_data_


def get_conflicts_dict(include_values: Optional[Dict[str, List[str]]] = None) -> 'model.flags.NRConflicts':
    """Creates a conflicts dict with the specified values."""
    conflicts_dict = model.flags.NRConflicts(
        need_zero=[],
        need_non_zero=[],
        preventing_flag_false=[],
        need_undefining=[],
        preventing_flag_undefine=[]
    )
    if include_values is not None:
        conflicts_dict.update(include_values)
    return conflicts_dict


def assert_nutrient_conflicts_equal(expected: 'model.flags.NRConflicts', actual: 'model.flags.NRConflicts') -> None:
    """Helper function to assert the nutrient conflicts are equal, regardless of the order of
    the contents of each list."""
    # noinspection PyTypedDict
    for category, nutrient_names in expected.items():
        # noinspection PyTypedDict
        unittest.TestCase.assertEqual(unittest.TestCase(), len(nutrient_names), len(actual[category]))
        # noinspection PyTypedDict
        unittest.TestCase.assertEqual(unittest.TestCase(), set(nutrient_names), set(actual[category]))


# The following is a selection of nutrient ratio data dicts to represent a range of flag-nutrient conflict scenarios.
FLAG_NR_SCENARIOS = {
    "foo_free_no_conflicts": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0.9, host_qty_g=100),
        "foobar": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.4, host_qty_g=100)
    },
    "foo_free_single_conflict": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobar": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.4, host_qty_g=100)
    },
    "foo_free_multiple_conflicts": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0.2, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0.9, host_qty_g=100),
        "foobar": qfx.get_qty_ratio_data(subject_qty_g=0.1, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.4, host_qty_g=100),
    },
    "foo_free_single_undefined": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0.9, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.4, host_qty_g=100),
    },
    "foo_free_multiple_undefined": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.4, host_qty_g=100),
    },
    "pongaterian_no_conflicts": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.2, host_qty_g=100),
        "tirbur": qfx.get_qty_ratio_data(subject_qty_g=0.3, host_qty_g=100),
    },
    "pongaterian_single_conflict": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0.1, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0.2, host_qty_g=100),
        "tirbur": qfx.get_qty_ratio_data(subject_qty_g=0.3, host_qty_g=100),
    },
    "pongaterian_multiple_conflicts": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0.2, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "tirbur": qfx.get_qty_ratio_data(subject_qty_g=0.3, host_qty_g=100),
    },
    "pongaterian_multiple_undefined": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
    },
    "pongaterian_single_undefined": {
        "foo": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "tirbur": qfx.get_qty_ratio_data(subject_qty_g=0.3, host_qty_g=100),
    },
    "tirbur_free_no_conflicts": {
        "tirbur": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
    },
    "tirbur_free_single_conflict": {
        "tirbur": qfx.get_qty_ratio_data(subject_qty_g=0.2, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
    },
    "bar_free_no_conflicts": {
        "bar": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
        "foobar": qfx.get_qty_ratio_data(subject_qty_g=0.2, host_qty_g=100),
        "bazing": qfx.get_qty_ratio_data(subject_qty_g=0, host_qty_g=100),
    }
}
