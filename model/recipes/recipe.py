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
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratios data for the instance."""

        # We're going to be cycling through ingredients, so to save recreating them,
        # create a cache to store them;
        ingredient_cache = {}

        # First, we need to figure out which nutrients are defined on all ingredients used
        # by the recipe.
        defined_nutrient_sets = []

        # Cycle through each ingredient;
        for idf_name in self.ingredient_quantities_data.keys():
            # Load the ingredient;
            i = model.ingredients.ReadonlyIngredient(ingredient_data_src=(model.ingredients.get_ingredient_data_src(
                for_df_name=idf_name
            )))
            # Cache the ingredient;
            ingredient_cache[idf_name] = i
            # Collect its nutrient ratio names;
            defined_nutrient_sets.append(set(i.defined_nutrient_ratio_names))

        # Grab the intersection of defined nutrient sets;
        common_nutrients = set.intersection(*defined_nutrient_sets)

        # OK, now we're going to work through each nutrient on the list of nutrients common to all
        # ingredients on the recipe, and figure out what its ratio is in the overall recipe.
        # First, create somewhere to put the nutrient ratios;
        nutrient_ratios: Dict[str, float] = {}

        # Now cycle through each ingredient, and use it to contribute its nutrient ratio based on its ratio;
        for idf_name, i in ingredient_cache.items():
            i_ratio: 'model.ingredients.ReadonlyIngredientRatio' = self.ingredient_ratios[idf_name]
            for nutrient_name in common_nutrients:
                nutrient_ratios[nutrient_name] += i.nutrient_ratios_data[nutrient_name] * i_ratio.g_per_subject_g

        # Return
        return nutrient_ratios

    @property
    def typical_serving_size_g(self) -> float:
        """Returns the typical serving size associated with this recipe."""
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
        return super().persistable_data


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
