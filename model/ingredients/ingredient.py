from typing import Optional, Dict, List, TypedDict, Union

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

    def __init__(self, ingredient_data: Optional[IngredientData] = None, **kwargs):
        super().__init__(**kwargs)

        # Init the blank nutrient ratios list;
        self._nutrient_ratios: Dict[str, 'nutrients.NutrientRatio'] = {
            nutr_name: nutrients.SettableNutrientRatio(nutr_name) for nutr_name in
            nutrients.configs.all_primary_nutrient_names}

        # Load any data that was provided;
        if ingredient_data is not None:
            self.load_data(ingredient_data)

    @property
    def name(self) -> Optional[str]:
        """Returns the name, which is also the unique value of an ingredient."""
        return self.unique_value

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Setter for the name. Ensures the name is unique before setting."""
        self.unique_value = name

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

    def get_nutrient_ratio(self, nutrient_name: str) -> 'nutrients.NutrientRatio':
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)
        return self._nutrient_ratios[nutrient_name]

    def _density_reset_cleanup(self) -> None:
        pass

    def _piece_mass_reset_cleanup(self) -> None:
        pass

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.ingredient_db_path

    def persistable_data(self) -> Dict[str, IngredientData]:
        # Compile the nutrients data;
        nutrients_data: Dict[str, 'nutrients.NutrientRatioData'] = {}
        for nutrient_name, nutrient_ratio in self._nutrient_ratios.items():
            nutrients_data[nutrient_name] = nutrients.NutrientRatioData(
                nutrient_g_per_subject_g=nutrient_ratio.g_per_subject_g,
                nutrient_pref_units=nutrient_ratio.pref_unit
            )

        return IngredientData(
            cost_per_g=self.cost_per_g,
            flags=self.flags_dof_data,
            name=self.name,
            nutrients=nutrients_data,
            bulk=self.bulk_data
        )

    def load_data(self, data: 'IngredientData') -> None:
        self: Union[Ingredient,
                    cost.SupportsSettableCost,
                    flags.HasSettableFlags,
                    nutrients.HasSettableNutrientRatios,
                    quantity.HasSettableBulk]
        self.cost_per_g = data['cost_per_g']
        self.set_flag_values(data['flags'])
        self.name = data['name']

        # Load the nutrient ratios data;
        for nutrient_name in data['nutrients']:
            self.set_nutrient_ratio(
                nutrient_name=nutrient_name,
                nutrient_qty=data['nutrients'][nutrient_name]['nutrient_g_per_subject_g'],
                nutrient_qty_unit='g',
                subject_qty=1,
                subject_qty_unit='g'
            )
            self.get_nutrient_ratio(nutrient_name).pref_unit = data['nutrients'][nutrient_name]['nutrient_pref_units']

        self.set_bulk_attrs(data['bulk'])
