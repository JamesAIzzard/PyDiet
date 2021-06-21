"""Defines utility functions for recipe module."""
from typing import Callable, Optional

import model
import persistence


def get_cost_per_g(recipe_data: 'model.recipes.RecipeData') -> float:
    """Returns the cost per gram for the recipe specified."""
    cost_per_g_sum: float = 0
    for ingredient_df_name in recipe_data['ingredient_quantities_data'].keys():
        ingredient_data = persistence.load_datafile(
            cls=model.ingredients.IngredientBase,
            datafile_name=ingredient_df_name
        )
        cost_per_g_sum += ingredient_data['cost_per_qty_data']['cost_per_g']

    # Average this cost and return;
    return cost_per_g_sum / len(recipe_data)


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


def get_recipe_data_src(
        for_unique_name: Optional[str] = None,
        for_df_name: Optional[str] = None
) -> Callable[[], 'model.recipes.RecipeData']:
    """Returns a source function for the data associated with the recipe indicated."""
    # Raise exception if both args are None;
    if for_unique_name is None and for_df_name is None:
        raise ValueError("Either datafile name or unique name must be specified.")

    # Convert the unique name into a df name;
    if for_unique_name is None:
        for_unique_name = get_unique_name_for_datafile_name(for_df_name)

    # Return the src function based on the df name;
    return lambda: persistence.load_datafile(
        cls=model.recipes.RecipeBase,
        unique_value=for_unique_name
    )
