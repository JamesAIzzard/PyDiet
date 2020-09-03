import copy
from typing import Optional, Dict, List, TypedDict, TYPE_CHECKING

from pydiet import nutrients, defining, quantity, cost, flags, quantity, persistence

if TYPE_CHECKING:
    from pydiet.cost.supports_cost import CostData
    from pydiet.quantity.supports_bulk import BulkData
    from pydiet.nutrients.supports_nutrients import NutrientData
    from pydiet.persistence.supports_persistence import PersistenceInfo


class IngredientData(TypedDict):
    cost: 'CostData'
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'NutrientData']
    bulk: 'BulkData'


def get_empty_ingredient_data() -> 'IngredientData':
    return IngredientData(cost=cost.supports_cost.get_empty_cost_data(),
                          flags=flags.supports_flags.get_empty_flags_data(),
                          name=None,
                          nutrients=nutrients.supports_nutrients.get_empty_nutrients_data(),
                          bulk=quantity.supports_bulk.get_empty_bulk_data())


class Ingredient(persistence.supports_persistence.SupportsPersistence,
                 defining.supports_definition.SupportsDefinition,
                 cost.supports_cost.SupportsCostSetting,
                 flags.supports_flags.SupportsFlagSetting,
                 nutrients.supports_nutrients.SupportsNutrients,
                 quantity.supports_bulk.SupportsBulk):

    def __init__(self, data: 'IngredientData', datafile_name:Optional[str]=None):
        self._data = data
        self._datafile_name = datafile_name

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    @name.setter
    def name(self, value: str) -> None:
        self._data['name'] = value

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        # Check name;
        if self.name == None:
            attr_names.append('name')
        # Check flags;
        if self.any_flag_undefined:
            for flag_name in self.undefined_flags:
                attr_names.append('{} flag'.format(
                    flag_name.replace('_', ' ')))
        # Check nutrients;
        # Check density;
        return attr_names

    @property
    def _cost_data(self) -> 'CostData':
        return self._data['cost']

    @property
    def _flags_data(self) -> Dict[str, Optional[bool]]:
        return self._data['flags']

    @property
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        return self._data['nutrients']

    @property
    def _bulk_data(self) -> 'BulkData':
        return self._data['bulk']

    @property
    def readonly_persistence_data(self) -> 'PersistenceInfo':
        return persistence.supports_persistence.PersistenceInfo(
            data=copy.deepcopy(self._data),
            datafile_name=self._datafile_name,
            unique_field_name='name',
            path_into_db=persistence.configs.ingredient_db_path
        )

    def set_datafile_name(self, datafile_name:str) -> None:
        self._datafile_name = datafile_name
