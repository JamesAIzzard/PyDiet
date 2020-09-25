import abc
import copy
from typing import Dict, Optional, TypedDict

from pydiet import nutrients


class NutrientData(TypedDict):
    nutrient_g_per_subject_g: Optional[float]
    nutrient_pref_units: str


def get_empty_nutrients_data() -> Dict[str, 'NutrientData']:
    nutrients_data = {}
    for nutrient_name in nutrients.configs.all_primary_nutrient_names:
        nutrients_data[nutrient_name] = NutrientData(nutrient_g_per_subject_g=None,
                                                     nutrient_pref_units='g')
    return nutrients_data


class SupportsNutrientContent(abc.ABC):

    @property
    @abc.abstractmethod
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        raise NotImplementedError

    @property
    def nutrients_data_copy(self) -> Dict[str, 'NutrientData']:
        return copy.deepcopy(self._nutrients_data)

    def get_nutrient_data_copy(self, nutrient_name: str) -> 'NutrientData':
        return self.nutrients_data_copy[nutrient_name]

    @property
    def nutrients_summary(self) -> str:
        return 'A nutrients summary.'


class SupportsSettingNutrientContent(SupportsNutrientContent, abc.ABC):

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
