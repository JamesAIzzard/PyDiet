from typing import Dict, Optional
from unittest import mock

import model

TEST_FLAG_DATA = {
    "foo_free": {
        "nutrient_relations": {
            "foo": model.flags.FlagImpliesNutrient.zero,
            "foobing": model.flags.FlagImpliesNutrient.zero,
            "foobar": model.flags.FlagImpliesNutrient.zero,
        },
        "direct_alias": True
    },
    "pongaterian": {
        "nutrient_relations": {},
        "direct_alias": False
    }
}

ALL_FLAGS = {}

class HasFlagsTestable(model.flags.HasFlags, model.nutrients.HasNutrientRatios):
    def __init__(self,
                 flag_dofs: Optional[Dict[str, Optional[bool]]] = None,
                 nutrient_ratios: Optional[Dict[str, 'mock.Mock']] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._flag_dofs_ = flag_dofs
        self._nutrient_ratios = nutrient_ratios

    @property
    def _flag_dofs(self) -> 'model.flags.FlagDOFData':
        return self._flag_dofs_

    @property
    def nutrient_ratios(self) -> Dict[str, 'mock.Mock']:
        return self._nutrient_ratios
