"""Defines recipe classes."""
import abc
from typing import Callable, Optional, Dict, List

import model
import persistence


class RecipeBase(
    model.HasReadableName,
    persistence.SupportsPersistence,
    abc.ABC
):
    """Abstract base class for readable and writbale recipe classes."""

    @staticmethod
    def get_path_into_db() -> str:
        """Returns the directory name in the database."""
        return f"{persistence.configs.path_into_db}/recipes"


class ReadableRecipe(
    RecipeBase,
    model.HasReadableName,
    model.ingredients.HasReadableIngredientQuantities,
    model.time.HasReadableServeTimes
):
    """Models a readable recipe."""

    def __init__(self, recipe_data_src: Callable[[], 'model.recipes.RecipeData'], **kwargs):
        super().__init__(**kwargs)

        self._recipe_data_src = recipe_data_src

    @property
    def _name(self) -> Optional[str]:
        """Returns the Recipe name."""
        return self._recipe_data_src()['name']

    @property
    def ingredient_quantities(self) -> Dict[str, 'model.ingredients.ReadonlyIngredientQuantity']:
        """Returns the readonly ingredient quantities on the instance."""
        # Grab the data from the src function;
        iq_data = self._recipe_data_src()['ingredient_quantities_data']

        # Create dict to compile the ingredient quantites;
        iq = {}

        # Define an accessor func for the data src;
        def i_data_src(df_name):
            """Accessor function for ingredient data src."""
            return lambda: iq_data[df_name]

        # Cycle through the data and init the ingredient quantities;
        for i_df_name, iqo_data in iq_data.items():
            iq[i_df_name] = model.ingredients.ReadonlyIngredientQuantity(
                ingredient=model.ingredients.ReadonlyIngredient(
                    ingredient_data_src=persistence.load_datafile(
                        cls=model.ingredients.IngredientBase,
                        datafile_name=i_df_name
                    )
                ),
                quantity_data_src=lambda: i_data_src(i_df_name)
            )

        # Return the dict;
        return iq

    @property
    def serve_times_data(self) -> List[str]:
        """Returns the serve times data for the instance."""
        return self._recipe_data_src()['serve_intervals']

    @property
    def unique_value(self) -> str:
        """Returns the unique name for the recipe."""
        return self._recipe_data_src()['name']


class SettableRecipe(
    RecipeBase,
    model.HasSettableName,
    model.ingredients.HasSettableIngredientQuantities,
    model.time.HasSettableServeTimes
):
    """Models a settable recipe."""

    def __init__(self, recipe_data: Optional['model.recipes.RecipeData'] = None, **kwargs):
        super().__init__(**kwargs)

        if recipe_data is not None:
            super().load_data(recipe_data)

    @model.HasReadableName.name.setter
    def name(self, name: Optional[str]) -> None:
        """Sets the name if unique to the recipe class, otherwise raises an exception."""
        # If the name is None, just set it and return;
        if name is None:
            self._name_ = name
            return

        # OK, the name isn't None, so we need to check if it is available;
        if persistence.check_unique_value_available(
                cls=self.__class__,
                proposed_value=name,
                ignore_datafile=self.datafile_name if self.datafile_name_is_defined else None
        ):
            # It is available, go ahead and set it;
            self._name_ = name
        # Otherwise, raise an exception;
        else:
            raise persistence.exceptions.UniqueValueDuplicatedError(duplicated_value=name)

    @property
    def unique_value(self) -> str:
        """Retrurns the unique value for the settable ingredient;"""
        return self._name
