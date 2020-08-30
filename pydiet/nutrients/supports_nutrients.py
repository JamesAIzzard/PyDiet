import abc
import copy
from typing import Dict, Optional, TypedDict

from pydiet import nutrients


class NutrientData(TypedDict):
    subject_mass_g: Optional[float]
    subject_qty_pref_units: Optional[str]
    nutrient_mass_g: Optional[float]
    nutrient_qty_pref_units: Optional[str]

def get_empty_nutrients_data() -> Dict[str, 'NutrientData']:
    nutrients_data = {}
    for nutrient_name in nutrients.global_nutrients.keys():
        nutrients_data[nutrient_name] = NutrientData(subject_mass_g=None,
                                                     subject_qty_pref_units=None,
                                                     nutrient_mass_g=None,
                                                     nutrient_qty_pref_units=None)
    return nutrients_data

class SupportsNutrients(abc.ABC):

    @abc.abstractproperty
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        raise NotImplementedError

    @property
    def readonly_nutrients_data(self) -> Dict[str, 'NutrientData']:
        return copy.deepcopy(self._nutrients_data)

    def get_readonly_nutrient_data(self, nutrient_name: str) -> 'NutrientData':
        return self.readonly_nutrients_data[nutrient_name]

    @property
    def nutrients_summary(self) -> str:
        return 'A nutrients summary.'

class SupportsNutrientsSetting(SupportsNutrients):

    def set_nutrient_data(self, nutrient_name: str,
                                      subject_mass_g: Optional[float],
                                      subject_qty_pref_units: Optional[str],
                                      nutrient_mass_g: Optional[float],
                                      nutrient_qty_pref_units: Optional[str]) -> None:

        def assign_values(data: 'NutrientData') -> None:
            data['subject_mass_g'] = subject_mass_g
            data['subject_qty_pref_units'] = subject_qty_pref_units
            data['nutrient_mass_g'] = nutrient_mass_g
            data['nutrient_qty_pref_units'] = nutrient_qty_pref_units

        # Take a backup of the dataset, make the change, and validate the dataset;
        whole_backup = self.readonly_nutrients_data
        nut_backup = whole_backup[nutrient_name]
        assign_values(nut_backup)
        nutrients.nutrients_service.validate_nutritients_data(
            nut_backup)

        # Make the change on the real dataset;
        nut_data = self._nutrients_data[nutrient_name]
        assign_values(nut_data)
