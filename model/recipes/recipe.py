"""Defines recipe classes."""
import abc
from typing import Callable, Optional, Dict, List, Any

import model
import persistence


class RecipeBase(
    model.HasReadableName,
    model.ingredients.HasReadableIngredientQuantities,
    model.time.HasReadableServeIntervals,
    model.instructions.HasReadableInstructionSrc,
    model.tags.HasReadableTags,
    persistence.SupportsPersistence,
    abc.ABC
):
    """Abstract base class for readable and writbale recipe classes."""

    @property
    def unique_value(self) -> str:
        """Returns the unique name of the recipe."""
        return self._name

    @property
    def typical_serving_size_g(self) -> float:
        """Returns the typical serving size associated with this recipe. This is the total of the ingredient
        quantities used to define the recipe."""
        total_mass = 0
        for ingredient_qty_data in self.ingredient_quantities_data.values():
            total_mass += ingredient_qty_data['quantity_in_g']
        return total_mass

    @staticmethod
    def get_path_into_db() -> str:
        """Returns the directory name in the database."""
        return f"{persistence.configs.PATH_INTO_DB}/recipes"

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the recipe instance."""
        data = super().persistable_data
        del data['nutrient_ratios_data']
        del data['cost_per_qty_data']
        return data


class ReadonlyRecipe(
    RecipeBase,
):
    """Models a readable recipe."""

    def __init__(self, recipe_data_src: Callable[[], 'model.recipes.RecipeData'], **kwargs):
        super().__init__(**kwargs)

        # Stash the data src function;
        self._recipe_data_src = recipe_data_src

        # Populate the datafile name;
        self._datafile_name = model.recipes.get_datafile_name_for_unique_value(
            unique_value=self._recipe_data_src()['name']
        )

    @property
    def _name(self) -> Optional[str]:
        """Returns the Recipe name."""
        return self._recipe_data_src()['name']

    @property
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for the instance."""
        return self._recipe_data_src()['ingredient_quantities_data']

    @property
    def serve_intervals_data(self) -> List[str]:
        """Returns the serve times data for the instance."""
        return self._recipe_data_src()['serve_intervals']

    @property
    def instruction_src(self) -> str:
        """Returns the instruction source for the recipe."""
        return self._recipe_data_src()['instruction_src']

    @property
    def tags(self) -> List[str]:
        """Returns the tags associated with the recipe."""
        return self._recipe_data_src()['tags']


class SettableRecipe(
    RecipeBase,
    model.HasSettableName,
    model.ingredients.HasSettableIngredientQuantities,
    model.time.HasSettableServeIntervals,
    model.instructions.HasSettableInstructionSrc,
    model.tags.HasSettableTags,
    persistence.CanLoadData
):
    """Models a settable recipe."""

    def __init__(self, recipe_data: Optional['model.recipes.RecipeData'] = None, **kwargs):
        super().__init__(**kwargs)

        if recipe_data is not None:
            super().load_data(recipe_data)

            # Populate the datafile name;
            self._datafile_name = persistence.get_datafile_name_for_unique_value(
                cls=model.recipes.RecipeBase,
                unique_value=self.name
            )

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

    def load_data(self, data: 'model.recipes.RecipeData') -> None:
        """Loads data into the isntance."""
        super().load_data(data)
