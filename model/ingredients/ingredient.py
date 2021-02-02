from typing import Optional, Dict, List, TypedDict

from model import nutrients, cost, flags, quantity, persistence, mandatory_attributes


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_g: Optional[float]
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'nutrients.NutrientRatioData']
    bulk: quantity.has_bulk.BulkData


class Ingredient(persistence.SupportsPersistence,
                 mandatory_attributes.HasMandatoryAttributes,
                 quantity.HasSettableBulk,
                 cost.SupportsSettableCost,
                 flags.HasSettableFlags,
                 nutrients.HasSettableNutrientRatios):

    def __init__(self, data: Optional[IngredientData] = None, **kwargs):
        super().__init__(**kwargs)
        # Init empty ingredient properties;
        self._cost_per_g: Optional[float] = None
        ...
        # Load any data that was provided;
        if data is not None:
            self.load_data(data)

    @property
    def name(self) -> Optional[str]:
        return self.get_unique_value()

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Setter for the name. Ensures the name is unique before setting."""
        self.set_unique_value(name)

    @property
    def missing_mandatory_attrs(self) -> List[str]:
        attr_names = []
        # Check name;
        if not self.name_is_defined:
            attr_names.append('name')
        # Check cost;
        if not self.cost_per_g_defined:
            attr_names.append('cost')
        # Check flag_data;
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
        return self._data['flag_data']

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
    def get_path_into_db() -> str:
        return persistence.configs.ingredient_db_path

    def persistable_data(self) -> Dict[str, Any]:
        ...

    def load_data(self, data: Dict[str, Any]) -> None:
        ...
