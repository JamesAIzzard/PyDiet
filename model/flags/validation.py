import model
import model.nutrients.main
from . import exceptions


def validate_configs(configs: 'model.flags.configs') -> None:
    """Validates the flag configuration file."""
    for flag_name, config in configs.FLAG_CONFIGS.items():
        # Check all related nutrient names are actually known nutrients;
        for nutrient_name in config['nutrient_relations'].keys():
            try:
                model.nutrients.main.validate_nutrient_name(nutrient_name)
            except model.nutrients.exceptions.NutrientNameNotRecognisedError:
                raise exceptions.UnknownRelatedNutrientError(nutrient_name=nutrient_name)

        # Check we don't have any direct alias relationships without any nutrients;
        if len(config['nutrient_relations']) == 0 and config['direct_alias'] is True:
            raise exceptions.DirectAliasWithoutRelatedNutrientsError(flag_name=flag_name)


def validate_flag_name(flag_name: str) -> str:
    """Returns validated flag name or raises exception.
    Raises:
        FlagNameError: To indicate the flag name is not recognised.
    """
    if flag_name in model.flags.ALL_FLAGS.keys():
        return str(flag_name)
    raise exceptions.FlagNameError(flag_name=flag_name)


def validate_flag_value(flag_value: bool) -> bool:
    """Returns validated flag value or raises exception.
    Raises:
        FlagValueError: To indicate the flag value is not valid.
    """
    if flag_value in [True, False]:
        return flag_value
    raise exceptions.FlagValueError(value=flag_value)
