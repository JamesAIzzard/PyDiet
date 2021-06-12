"""Defines utility functions for ingredient module."""
from typing import Callable, Optional

import model.ingredients
import persistence
from model import ingredients


def get_ingredient_name_from_df_name(datafile_name: str) -> str:
    """Returns the ingredient name corresponding to the datafile name."""
    return persistence.get_unique_value_from_datafile_name(cls=ingredients.ReadonlyIngredient,
                                                           datafile_name=datafile_name)


def get_ingredient_data_src(
        for_unique_name: Optional[str] = None,
        for_df_name: Optional[str] = None
) -> Callable[[], 'model.ingredients.IngredientData']:
    """Returns an ingredient data src function."""
    # Get the datafile name for the ingredient we want;
    df_name = for_df_name
    if for_df_name is None:
        df_name = persistence.get_datafile_name_for_unique_value(
            cls=model.ingredients.IngredientBase,
            unique_value=for_unique_name
        )

    # Return a source function that will grab it;
    return lambda: persistence.load_datafile(
        cls=model.ingredients.IngredientBase,
        datafile_name=df_name
    )
