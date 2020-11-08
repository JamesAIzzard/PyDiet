from typing import Optional, Dict, List, TypedDict, TYPE_CHECKING

from pydiet import nutrients, completion, cost, flags, quantity, persistence

if TYPE_CHECKING:
    from pydiet.quantity.has_bulk import BulkData
    from pydiet.nutrients.has_nutrient_ratios import NutrientData
    from pydiet.persistence.supports_persistence import DBInfo, PersistenceInfo


class IngredientData(TypedDict):
    cost_per_g: Optional[float]
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'NutrientData']
    bulk: quantity.has_bulk.BulkData


def get_empty_ingredient_data() -> 'IngredientData':
    return IngredientData(cost_per_g=None,
                          flags=flags.supports_flags.get_empty_flags_data(),
                          name=None,
                          nutrients=nutrients.has_nutrient_ratios.get_empty_nutrients_data(),
                          bulk=quantity.has_bulk.get_empty_bulk_data())


def load_new_ingredient() -> 'Ingredient':
    """Creates and returns a fresh ingredient instance with no data filled in."""
    return Ingredient(get_empty_ingredient_data())


def get_ingredient_name(datafile_name: str) -> str:
    """Returns the ingredient name corresponding to the datafile name."""
    return persistence.get_unique_val_from_df_name(cls=Ingredient, datafile_name=datafile_name)


class Ingredient(persistence.supports_persistence.SupportsPersistence,
                 completion.has_mandatory_attributes.SupportsCompletion,
                 completion.supports_name.SupportsNameSetting,
                 cost.supports_cost.SupportsCostSetting,
                 flags.supports_flags.SupportsFlagSetting,
                 nutrients.has_nutrient_ratios.SupportsSettingNutrientContent,
                 quantity.has_bulk.SupportsBulkSetting):

    def __init__(self, data: 'IngredientData', datafile_name: Optional[str] = None):
        self._data = data
        self._datafile_name = datafile_name

    @property
    def name(self) -> Optional[str]:
        return self._data['name']

    def set_name(self, name: Optional[str]) -> None:
        self.set_unique_field(name)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        # Check name;
        if not self.name_is_defined:
            attr_names.append('name')
        # Check cost;
        if not self.cost_per_g_defined:
            attr_names.append('cost')
        # Check flags;
        if self.any_flag_undefined:
            for flag_name in self.unset_flags:
                attr_names.append('{} flag'.format(
                    flag_name.replace('_', ' ')))
        # Check nutrients;
        for nutrient_name in nutrients.configs.mandatory_nutrient_names:
            if not self.nutrient_is_defined(nutrient_name):
                attr_names.append(nutrient_name)
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
