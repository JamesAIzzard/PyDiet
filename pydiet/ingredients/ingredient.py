from typing import Optional, Dict, List, TypedDict, TYPE_CHECKING

from pydiet import nutrients, defining, cost, flags, quantity, persistence

if TYPE_CHECKING:
    from pydiet.quantity.supports_bulk import BulkData
    from pydiet.nutrients.supports_nutrients import NutrientData
    from pydiet.persistence.supports_persistence import DBInfo, PersistenceInfo


class IngredientData(TypedDict):
    cost_per_g: Optional[float]
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'NutrientData']
    bulk: quantity.supports_bulk.BulkData


def get_empty_ingredient_data() -> 'IngredientData':
    return IngredientData(cost_per_g=None,
                          flags=flags.supports_flags.get_empty_flags_data(),
                          name=None,
                          nutrients=nutrients.supports_nutrients.get_empty_nutrients_data(),
                          bulk=quantity.supports_bulk.get_empty_bulk_data())


class Ingredient(persistence.supports_persistence.SupportsPersistence,
                 defining.supports_definition.SupportsDefinition,
                 defining.supports_name.SupportsNameSetting,
                 cost.supports_cost.SupportsCostSetting,
                 flags.supports_flags.SupportsFlagSetting,
                 nutrients.supports_nutrients.SupportsNutrients,
                 quantity.supports_bulk.SupportsBulkSetting):

    def __init__(self, data: 'IngredientData', datafile_name: Optional[str] = None):
        self._data = data
        self._datafile_name = datafile_name

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    def set_name(self, name: Optional[str]) -> None:
        self._data['name'] = name

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        # Check name;
        if not self.name_is_defined:
            attr_names.append('name')
        # Check flags;
        if self.any_flag_undefined:
            for flag_name in self.unset_flags:
                attr_names.append('{} flag'.format(
                    flag_name.replace('_', ' ')))
        # Check nutrients;
        # Check density;
        return attr_names

    @property
    def cost_per_g(self) -> Optional[float]:
        return self._data['cost_per_g']

    def _set_cost_per_g(self, validated_cost_per_g: Optional[float]) -> None:
        self._data['cost_per_g'] = validated_cost_per_g

    @property
    def _flags_data(self) -> Dict[str, Optional[bool]]:
        return self._data['flags']

    @property
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        return self._data['nutrients']

    @property
    def _bulk_data(self) -> 'BulkData':
        return self._data['bulk']

    def _density_reset_cleanup(self) -> None:
        pass

    def _piece_mass_reset_cleanup(self) -> None:
        pass

    @staticmethod
    def get_db_info() -> 'DBInfo':
        return persistence.supports_persistence.DBInfo(
            unique_field_name='name',
            path_into_db=persistence.configs.ingredient_db_path
        )

    @property
    def _persistence_info(self) -> 'PersistenceInfo':
        return persistence.supports_persistence.PersistenceInfo(
            data=self._data,
            datafile_name=self._datafile_name
        )

    def set_datafile_name(self, datafile_name: str) -> None:
        self._datafile_name = datafile_name
