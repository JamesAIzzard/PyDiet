import abc
from typing import Dict, List, cast, TYPE_CHECKING

from pydiet import nutrients
from pydiet.nutrients import configs
from pydiet.quantity import HasBulk

if TYPE_CHECKING:
    from pydiet.nutrients import NutrientRatio


class HasNutrientRatios(HasBulk, abc.ABC):

    def __init__(self, **kwds):
        super().__init__(**kwds)

    @abc.abstractmethod
    def get_nutrient_ratio(self, nutrient_name: str) -> 'NutrientRatio':
        """Returns a NutrientRatio by name."""
        raise NotImplementedError

    @property
    def nutrient_ratios(self) -> Dict[str, 'NutrientRatio']:
        """Returns all nutrient ratios (defined & undefined) by their primary names."""
        nutrient_ratios = {}
        for nutrient_name in configs.all_primary_nutrient_names:
            nutrient_ratios[nutrient_name] = self.get_nutrient_ratio(nutrient_name)
        return nutrient_ratios

    @property
    def defined_optional_nutrient_names(self) -> List[str]:
        """Returns a list of the optional nutrient names which have been defined."""
        defined_optionals = []
        for nutrient_name, nutrient_ratio in self.nutrient_ratios.items():
            if nutrient_name not in nutrients.configs.mandatory_nutrient_names and nutrient_ratio.defined:
                defined_optionals.append(nutrient_name)
        return defined_optionals

    @property
    def nutrients_summary(self) -> str:
        """Returns a readable summary of all mandatory and additionally defined nutrients."""
        output = ''
        for nutrient_name in configs.mandatory_nutrient_names + self.defined_optional_nutrient_names:
            output = output + '{name:<30} {summary:<30}\n'.format(
                name=nutrient_name.replace('_', ' ') + ':',
                summary=self.get_nutrient_ratio(nutrient_name).summary
            )
        return output


class HasSettableNutrientRatios(HasNutrientRatios, abc.ABC):

    @abc.abstractmethod
    def get_nutrient_ratio(self, nutrient_name: str) -> 'NutrientRatio':
        """Returns a SettableNutrientRatio by name."""
        raise NotImplementedError

    def set_nutrient_ratio(self, nutrient_name: str, nutrient_qty: float, nutrient_qty_unit: str, subject_qty: float,
                           subject_qty_unit: str) -> None:
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
