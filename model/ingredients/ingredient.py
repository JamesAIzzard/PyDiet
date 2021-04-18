from typing import Optional, Dict, List, TypedDict, Union

import model.quantity
from model import nutrients, cost, flags, quantity, mandatory_attributes
import persistence


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

    @property
    def density_units_in_use(self) -> bool:
        if self.pref_unit in model.quantity.get_recognised_vol_units():
            return True
        return False

    @property
    def piece_mass_units_in_use(self) -> bool:
        if self.pref_unit in model.quantity.get_recognised_pc_units():
            return True
        return False

    def __init__(self, ingredient_data: Optional[IngredientData] = None, **kwargs):
        super().__init__(**kwargs)

        # Init the blank nutrient ratios list;
        self._nutrient_ratios: Dict[str, 'nutrients.SettableNutrientRatio'] = {
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

    def _get_settable_nutrient_ratio(self, nutrient_name: str) -> 'nutrients.SettableNutrientRatio':
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)
        return self._nutrient_ratios[nutrient_name]

    def get_nutrient_ratio(self, nutrient_name: str) -> 'nutrients.NutrientRatio':
        """See note on parent class. It is important not to give out settable nutrient ratios
        becuase that would allow them to be set without triggering mutual validation against
        all the nutrients in the set.
        """
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)
        # Grab the settable instance and convert it to a non-settable;
        settable_nr = self._nutrient_ratios[nutrient_name]
        non_settable_nr = nutrients.NutrientRatio(
            nutrient_name=settable_nr.nutrient.primary_name,
            g_per_subject_g=settable_nr.g_per_subject_g,
            pref_unit=settable_nr.pref_unit
        )
        return non_settable_nr

    def _density_reset_cleanup(self) -> None:
        s: Union['model.quantity.HasSettableBulk', 'model.nutrients.HasSettableNutrientRatios'] = self
        if self.pref_unit in model.quantity.get_recognised_vol_units():
            s.pref_unit = 'g'
            s.ref_qty = 100
        for nutrient_ratio in self.nutrient_ratios.values():
            if nutrient_ratio.pref_unit in model.quantity.get_recognised_mass_units():
                s.set_nutrient_pref_unit(nutrient_ratio.nutrient.primary_name, "g")

    def _piece_mass_reset_cleanup(self) -> None:
        s: Union['model.quantity.HasSettableBulk', 'model.nutrients.HasSettableNutrientRatios'] = self
        if self.pref_unit in model.quantity.get_recognised_pc_units():
            s.pref_unit = 'g'
            s.ref_qty = 100
        for nutrient_ratio in self.nutrient_ratios.values():
            if nutrient_ratio.pref_unit in model.quantity.get_recognised_pc_units():
                s.set_nutrient_pref_unit(nutrient_ratio.nutrient.primary_name, "g")

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
        # Clarify parents for intellisense;
        self: Union[Ingredient,
                    cost.SupportsSettableCost,
                    flags.HasSettableFlags,
                    nutrients.HasSettableNutrientRatios,
                    quantity.HasSettableBulk]

        self.name = data['name']

        # Bulk data should be set before we start filling in data which might
        # rely on the bulk properties;
        self.set_bulk_data(data['bulk'])

        self.cost_per_g = data['cost_per_g']

        # Load the nutrient ratios data;
        for nutrient_name in data['nutrients']:
            self.set_nutrient_ratio(
                nutrient_name=nutrient_name,
                nutrient_qty=data['nutrients'][nutrient_name]['nutrient_g_per_subject_g'],
                nutrient_qty_unit='g',
                subject_qty=1,
                subject_qty_unit='g'
            )
            self._get_settable_nutrient_ratio(nutrient_name).pref_unit = data['nutrients'][nutrient_name][
                'nutrient_pref_units']

        # Set flags after nutrients;
        # (We may get conflicts if flags imply not yet defined nutrient values);
        self.set_flag_data(data['flags'])
