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
                          nutrient_g_per_subject_g: Optional[float],
                          nutrient_pref_units: str = 'g') -> None:

        new_data = NutrientData(nutrient_g_per_subject_g=nutrient_g_per_subject_g,
                                nutrient_pref_units=nutrient_pref_units)

        # Make the change on a copy of the data and validate it;
        nutrients_dataset_copy = self.nutrients_data_copy
        nutrients_dataset_copy[nutrient_name] = new_data
        nutrients.supports_nutrient_content.validate_nutrients_data(nutrients_dataset_copy)

        # All OK, so make the change on the real dataset;
        self._nutrients_data[nutrient_name] = new_data


