from model import ingredients
import persistence


def get_ingredient_name(datafile_name: str) -> str:
    """Returns the ingredient name corresponding to the datafile name."""
    return persistence.get_unique_value_from_datafile_name(cls=ingredients.Ingredient, datafile_name=datafile_name)
