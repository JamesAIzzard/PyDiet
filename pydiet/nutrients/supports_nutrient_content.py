import abc
import copy
from typing import Dict, List, Optional, cast, TypedDict

from pydiet import nutrients, quantity


class NutrientData(TypedDict):
    nutrient_g_per_subject_g: Optional[float]
    nutrient_pref_units: str


def get_empty_nutrients_data() -> Dict[str, 'NutrientData']:
    nutrients_data = {}
    for nutrient_name in nutrients.configs.all_primary_nutrient_names:
        nutrients_data[nutrient_name] = NutrientData(nutrient_g_per_subject_g=None,
                                                     nutrient_pref_units='g')
    return nutrients_data


class SupportsNutrientContent(quantity.supports_bulk.SupportsBulk, abc.ABC):

    @property
    @abc.abstractmethod
    def _nutrients_data(self) -> Dict[str, 'NutrientData']:
        raise NotImplementedError

    @property
    def nutrients_data_copy(self) -> Dict[str, 'NutrientData']:
        return copy.deepcopy(self._nutrients_data)

    def get_nutrient_data_copy(self, nutrient_name: str) -> 'NutrientData':
        return self.nutrients_data_copy[nutrient_name]

    def nutrient_is_defined(self, nutrient_name: str) -> bool:
        # Convert alias
        nutrient_name = nutrients.nutrients_service.get_nutrient_primary_name(nutrient_name)
        nutrient_data = self._nutrients_data[nutrient_name]
        if None in nutrient_data.values():
            return False
        else:
            return True

    @property
    def defined_optional_nutrient_names(self) -> List[str]:
        defined_nutrient_names = []
        for nutrient_name in self._nutrients_data:
            if nutrient_name not in nutrients.configs.mandatory_nutrient_names and self.nutrient_is_defined(
                    nutrient_name):
                defined_nutrient_names.append(nutrient_name)
        return defined_nutrient_names

    def summarise_nutrient(self, nutrient_name: str) -> str:
        nutrient_name = nutrients.nutrients_service.get_nutrient_primary_name(nutrient_name)
        nutrient_data = self._nutrients_data[nutrient_name]
        nutrient_g_per_subject_g = nutrient_data['nutrient_g_per_subject_g']
        nutrient_pref_unit = nutrient_data['nutrient_pref_units']
        if None in nutrient_data.values():
            return 'Undefined'
        else:
            nutr_ref_qty_g = nutrient_g_per_subject_g * self.ref_qty_in_g
            nutr_ref_qty = quantity.quantity_service.convert_qty_unit(qty=nutr_ref_qty_g,
                                                                      start_unit='g',
                                                                      end_unit=nutrient_pref_unit)
            return '{nutr_qty:.3f}{nutr_unit} per {subj_qty}{subj_unit}'.format(
                nutr_qty=nutr_ref_qty,
                nutr_unit=nutrient_pref_unit,
                subj_qty=self.ref_qty,
                subj_unit=self.pref_unit
            )

    @property
    def nutrients_summary(self) -> str:
        output = ''
        for nutrient_name in nutrients.configs.mandatory_nutrient_names + self.defined_optional_nutrient_names:
            output = output + '{name:<30} {summary:<30}\n'.format(
                name=nutrient_name.replace('_', ' ') + ':',
                summary=self.summarise_nutrient(nutrient_name)
            )
        return output


class SupportsSettingNutrientContent(SupportsNutrientContent, abc.ABC):

    def set_nutrient_data(self, nutrient_name: str, nutrient_data: 'NutrientData') -> None:
        nutrient_name = nutrients.nutrients_service.get_nutrient_primary_name(nutrient_name)

        nutrient_data = nutrients.validation.validate_nutrient_data(nutrient_data)

        # Make the change on a copy of the data and validate it;
        nutrients_data_copy = self.nutrients_data_copy
        nutrients_data_copy[nutrient_name] = nutrient_data
        nutrients.validation.validate_nutrients_data(nutrients_data_copy)

        # All OK, so make the change on the real dataset;
        self._nutrients_data[nutrient_name] = nutrient_data

        # If there is a flag related, set it;
        # Nasty hack to avoid circular import; A better way to do this would be to have a base class which mixes
        # nutrients, flags, bulk, etc, which ingredient and recipe would then inherit.
        nself = cast('flags.supports_flags.SupportsFlagSetting', self)
        for flag_name in nutrients.configs.nutrient_flag_rels:
            if nutrient_name in nutrients.configs.nutrient_flag_rels[flag_name]:
                if nutrient_data['nutrient_g_per_subject_g'] == 0:
                    # noinspection PyProtectedMember
                    nself._flags_data[flag_name] = True
                else:
                    # noinspection PyProtectedMember
                    nself._flags_data[flag_name] = False

    def set_nutrients_data(self, nutrients_data: Dict[str, 'NutrientData']) -> None:
        validated_nutrients_data = nutrients.validation.validate_nutrients_data(nutrients_data)
        for nutrient_name in self._nutrients_data:
            self._nutrients_data[nutrient_name] = validated_nutrients_data[nutrient_name]

    def reset_nutrient(self, nutrient_name: str) -> None:
        nutrient_name = nutrients.nutrients_service.get_nutrient_primary_name(nutrient_name)
        self._nutrients_data[nutrient_name] = NutrientData(
            nutrient_g_per_subject_g=None,
            nutrient_pref_units='g'
        )
