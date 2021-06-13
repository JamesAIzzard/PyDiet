"""Defines utility functions for recipe module."""
from typing import Callable

import model
import persistence


def get_unique_name_for_datafile_name(df_name: str) -> str:
    """Returns the unique recipe name corresponding to the datafile name provided."""
    return persistence.get_unique_value_from_datafile_name(
        cls=model.recipes.RecipeBase,
        datafile_name=df_name
    )


def get_datafile_name_for_unique_value(unique_value: str) -> str:
    """Returns the recipe datafile name corresponding to the unique name provided."""
    return persistence.get_datafile_name_for_unique_value(
        cls=model.recipes.RecipeBase,
        unique_value=unique_value
    )


def get_recipe_data_src(for_unique_name: str) -> Callable[[], 'model.recipes.RecipeData']:
    """Returns a source function for the data associated with the recipe indicated."""
    return lambda: persistence.load_datafile(
        cls=model.recipes.RecipeBase,
        unique_value=for_unique_name
    )
