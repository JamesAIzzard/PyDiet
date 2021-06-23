"""Test fixtures for the recipe module."""
from typing import List, Optional

import model
import persistence


class RecipeBaseTestable(model.recipes.RecipeBase):
    """Minimal implementation to allow testing of RecipeBase class."""

    def __init__(self, recipe_data: 'model.recipes.RecipeData'):
        super().__init__()
        self._recipe_data = recipe_data

    @property
    def _name(self) -> Optional[str]:
        """Returns the recipe name."""
        return self._recipe_data['name']

    @property
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for the instance."""
        return self._recipe_data['ingredient_quantities_data']

    @property
    def serve_intervals_data(self) -> List[str]:
        """Returns the serve times for the instance."""
        return self._recipe_data['serve_intervals']

    @property
    def instruction_src(self) -> str:
        """Returns the instruction source for the instnace."""
        return self._recipe_data['instruction_src']

    @property
    def tags(self) -> List[str]:
        """Returns the tags associated with the instance."""
        return self._recipe_data['tags']

    @property
    def unique_value(self) -> str:
        """Returns the unique value use for persisting the instance."""
        return self._name


class HasReadableRecipeRatiosTestable(model.recipes.HasReadableRecipeRatios):
    """Minimal implementation to allow testing of HasReadableRecipeRatios class."""

    def __init__(self, recipe_ratios_data: 'model.recipes.RecipeRatiosData', **kwargs):
        super().__init__(**kwargs)

        self._recipe_ratios_data = recipe_ratios_data

    @property
    def recipe_ratios_data(self) -> 'model.recipes.RecipeRatiosData':
        """Returns the recipe ratios data."""
        return self._recipe_ratios_data


def get_recipe_data(for_unique_name: Optional[str] = None) -> 'model.recipes.RecipeData':
    """Grabs the recipe data for the recipe specified."""
    # If the unique name was specified, load and return the data for it;
    if for_unique_name is not None:
        return persistence.load_datafile(
            cls=model.recipes.RecipeBase,
            unique_value=for_unique_name
        )

    # OK, no special case, so just return empty data with defaults;
    return model.recipes.RecipeData(
        name=None,
        ingredient_quantities_data={},
        serve_intervals=[],
        instruction_src=None,
        tags=[]
    )
