from typing import Dict, Optional
from unittest import mock

import model
from tests.model.nutrients import fixtures as nutfx
# Import test configs to allow us to build the global test flag list;
from . import test_configs

# Validate the test flag configs (using the test nutrients);
with mock.patch('model.nutrients.validation.PRIMARY_AND_ALIAS_NUTRIENT_NAMES', nutfx.PRIMARY_AND_ALIAS_NUTRIENT_NAMES):
    nutfx.use_test_nutrients(model.flags.validation.validate_configs(test_configs))

# Build the global flag list for testing, using the test configs;
with mock.patch('model.flags.flag.configs', test_configs), \
        mock.patch('model.flags.main.configs', test_configs):
    ALL_FLAGS: Dict[str, 'model.flags.Flag'] = model.flags.build_global_flag_list()


# Create a decorator to look after the patching required to run the test flags;
def use_test_flags(func):
    @mock.patch('model.flags.ALL_FLAGS', ALL_FLAGS)
    @mock.patch('model.flags.flag.configs', test_configs)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper


class HasFlagsTestable(model.flags.HasFlags):
    def __init__(self,
                 flag_dofs: Optional[Dict[str, Optional[bool]]] = None,
                 nutrient_ratios: Optional[Dict[str, 'mock.Mock']] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._flag_dofs_ = flag_dofs if flag_dofs is not None else {}
        self._nutrient_ratios = nutrient_ratios if nutrient_ratios is not None else {}

    @property
    def _flag_dofs(self) -> 'model.flags.FlagDOFData':
        return self._flag_dofs_

    @property
    def nutrient_ratios(self) -> Dict[str, 'mock.Mock']:
        return self._nutrient_ratios


def get_mock_nutrient_ratio(nutrient_name: str, g_per_subject_g: float) -> 'mock.Mock':
    nr = mock.Mock()
    nr.g_per_subject_g = g_per_subject_g
    nr.nutrient_name = nutrient_name
    nr.persistable_data = {}
    return nr
