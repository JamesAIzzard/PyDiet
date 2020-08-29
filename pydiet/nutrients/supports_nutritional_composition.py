import abc
from typing import Dict, Optional, TypedDict, Protocol

from pydiet import nutrients

class NutrientCompositionData(TypedDict):
    subject_mass_g: Optional[float]
    subject_qty_pref_units: Optional[str]
    nutrient_mass_g: Optional[float]
    nutrient_qty_pref_units: Optional[str]


nutrient_composition_data_template: 'NutrientCompositionData' = {
    "subject_mass_g": None,
    "subject_qty_pref_units": None,
    "nutrient_mass_g": None,
    "nutrient_qty_pref_units": None
}


class SupportsNutritionalComposition(Protocol):

    @abc.abstractproperty
    def readonly_nutritional_composition_data(self) -> Dict[str, 'NutrientCompositionData']:
        raise NotImplementedError

    def get_readonly_nutrient_composition_data(self, nutrient_name: str) -> 'NutrientCompositionData':
        return self.readonly_nutritional_composition_data[nutrient_name]


class SupportsNutritionalCompositionSetting(SupportsNutritionalComposition, Protocol):

    @abc.abstractproperty
    def nutritional_composition_data(self) -> Dict[str, 'NutrientCompositionData']:
        raise NotImplementedError

    def set_nutrient_composition_data(self, nutrient_name: str,
                                      subject_mass_g: Optional[float],
                                      subject_qty_pref_units: Optional[str],
                                      nutrient_mass_g: Optional[float],
                                      nutrient_qty_pref_units: Optional[str]) -> None:
        # Take a backup of the dataset, make the change, and validate the dataset;
        def assign_values(data:'NutrientCompositionData') -> None:
            data['subject_mass_g'] = subject_mass_g
            data['subject_qty_pref_units'] = subject_qty_pref_units
            data['nutrient_mass_g'] = nutrient_mass_g
            data['nutrient_qty_pref_units'] = nutrient_qty_pref_units
        whole_backup = self.readonly_nutritional_composition_data.deepcopy()
        nut_backup = whole_backup[nutrient_name]            
        assign_values(nut_backup)
        nutrients.nutrients_service.validate_nutritional_composition_data(nut_backup)

        # Make the change on the real dataset;
        nut_data = self.nutritional_composition_data[nutrient_name]
        assign_values(nut_data)
