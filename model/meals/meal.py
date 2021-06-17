"""Defines meal classes."""
from typing import List, Dict, Callable, Optional, Any

import model
import persistence


class SettableMeal(persistence.YieldsPersistableData, persistence.CanLoadData):
    """Models a collection of recipes (combined to form a meal)."""

    def __init__(self, meal_data: Optional['model.meals.MealData'] = None):

        # Stash the meal data passed in during init;
        self._meal_data = {}

        if meal_data is not None:
            self.load_data(meal_data)

    def add_recipe(self, recipe_unique_name: str, recipe_qty_data: 'model.quantity.QuantityData') -> None:
        """Adds a recipe to the meal instance."""
        self._meal_data[model.recipes.get_datafile_name_for_unique_value(recipe_unique_name)] = recipe_qty_data

    @property
    def total_meal_mass_g(self) -> float:
        """Returns the sum of all recipe quantities on this meal."""
        # Create somewhere to put the rolling total;
        total_meal_mass: float = 0

        # Roll up the total qty;
        for qty_data in self._meal_data.values():
            total_meal_mass += qty_data['quantity_in_g']

        # Return the result;
        return total_meal_mass

    @property
    def recipes(self) -> List['model.recipes.ReadonlyRecipe']:
        """Returns the list of recipe instances associated with this meal."""
        # Create somewhere to put the recipes;
        recipes = []

        # Cycle through the recipe datafile names in the meal data dict;
        for recipe_df_name in self._meal_data.keys():
            # And add the recipe instance to represent it to the list to return;
            recipes.append(model.recipes.ReadonlyRecipe(
                recipe_data_src=model.recipes.get_recipe_data_src(
                    for_df_name=recipe_df_name
                )
            ))

        # All done, return the list;
        return recipes

    @property
    def recipe_quantities(self) -> Dict[str, 'model.recipes.SettableRecipeQuantity']:
        """Returns the recipe quantities associated with this meal."""
        # Create somewhere to compile the quantities;
        _recipe_quantities = {}

        # Cycle through the meal data and populate the quantities;
        for recipe_df_name, recipe_qty_data in self._meal_data.items():
            _recipe_quantities[recipe_df_name] = model.recipes.SettableRecipeQuantity(
                recipe=model.recipes.ReadonlyRecipe(
                    recipe_data_src=model.recipes.get_recipe_data_src(for_df_name=recipe_df_name)
                ),
                quantity_data=recipe_qty_data
            )

        # Return the data;
        return _recipe_quantities

    @property
    def recipe_ratios(self) -> Dict[str, 'model.recipes.ReadonlyRecipeRatio']:
        """Returns the recipe ratios associated with this meal."""
        # Somewhere to compile the ratios;
        _recipe_ratios = {}

        # Grab the recipe quantities from the meal data;
        _recipe_quantities = self.recipe_quantities

        # Cache the sum of all recipes masses on the instance;
        total_meal_mass_g = self.total_meal_mass_g

        # Define a factory function to create accessors for the src data on this instnace;
        def get_qty_ratio_data_src(rdf: str) -> Callable[[], 'model.quantity.QuantityRatioData']:
            """Returns an accessor function for the quantity data associated with the
            specified recipe df name."""
            return lambda: model.quantity.QuantityRatioData(
                subject_qty_data=self._meal_data[rdf],
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=total_meal_mass_g,
                    pref_unit='g'
                )
            )

        # Cycle through the data, compiling the ratios;
        for recipe_df_name, recipe_qty_data in self._meal_data.items():
            _recipe_ratios[recipe_df_name] = model.recipes.ReadonlyRecipeRatio(
                recipe=model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
                    for_df_name=recipe_df_name
                )),
                ratio_host=self,
                qty_ratio_data_src=get_qty_ratio_data_src(recipe_df_name)
            )

        return _recipe_ratios

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for this meal instance."""
        return self._meal_data

    def load_data(self, meal_data: 'model.meals.MealData') -> None:
        """Loads data into the instance."""
        self._meal_data = meal_data
