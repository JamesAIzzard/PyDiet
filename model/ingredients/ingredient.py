from typing import Optional, Dict, List, TypedDict

from model import nutrients, cost, flags, quantity, persistence, mandatory_attributes


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_g: Optional[float]
    flags: Dict[str, Optional[bool]]
    name: Optional[str]
    nutrients: Dict[str, 'nutrients.NutrientRatioData']
    bulk: quantity.BulkData


class Ingredient(persistence.SupportsPersistence,
                 mandatory_attributes.HasMandatoryAttributes,
                 quantity.HasSettableBulk,
                 cost.SupportsSettableCost,
                 flags.HasSettableFlags,
                 nutrients.HasSettableNutrientRatios):

    def __init__(self, data: Optional[IngredientData] = None, **kwargs):
        super().__init__(**kwargs)
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
    def name_is_defined(self) -> bool:
        """Returns True/False to indicate if the ingredient name has been defined."""
        return self.unique_value_defined

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
        attr_names = attr_names + self.undefined_mandatory_nutrient_ratios
        return attr_names

    def _density_reset_cleanup(self) -> None:
        pass

    def _piece_mass_reset_cleanup(self) -> None:
        pass

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.ingredient_db_path

    def persistable_data(self) -> Dict[str, IngredientData]:
        return IngredientData(
            cost_per_g=self.cost_per_g,
            flags=self.flags_data,
            name=self.name,
            nutrients=self.nutrient_ratios_data,
            bulk=self.bulk_data
        )

    def load_data(self, data: IngredientData) -> None:
        super().cost_per_g = data['cost_per_g']
        self.set_flags(data['flags'])
        self.name = data['name']
        self.set_nutrient_ratios(data['nutrients'])
        self.set_bulk_attrs(data['bulk'])
