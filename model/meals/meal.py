"""Defines meal classes."""
from typing import List, Dict, Callable, Optional, Any

import model
import persistence


class SettableMeal(
    model.nutrients.HasReadableNutrientRatios,
    persistence.YieldsPersistableData,
    persistence.CanLoadData
):
    """Models a collection of recipes (combined to form a meal)."""

    def __init__(self, meal_data: Optional['model.meals.MealData'] = None):

        # Stash the meal data passed in during init;
        self._meal_data = {}

        if meal_data is not None:
            self.load_data(meal_data)

    @property
    def cost_gbp_per_g(self) -> float:
        """Returns the cost_per_g for the meal."""
        return model.meals.get_cost_per_g(meal_data=self._meal_data)

    def get_flag_value(self, flag_name:str) -> Optional[bool]:
        """Returns True/False to indicate the value of the named flag."""
        return model.meals.get_flag_value(flag_name=flag_name, meal_data=self._meal_data)

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratios data for the instance."""

        # Create vars to store useful things;
        defined_nutrient_sets = []
        recipes = []

        # Cycle through each recipe;
        for rdf_name in self._meal_data.keys():
            # Load it;
            r = model.recipes.ReadonlyRecipe(
                recipe_data_src=model.recipes.get_recipe_data_src(for_df_name=rdf_name)
            )
            recipes.append(r)
            # Add its defined nutrients to the set list;
            defined_nutrient_sets.append(set(r.defined_nutrient_ratio_names))

        # Grab the intersection of defined nutrient sets;
        common_nutrients = set.intersection(*defined_nutrient_sets)

        # Create somewhere to put the nutrient ratios;
        nutrient_ratios = {}

        # For each common nutrient, average across each ingredient;
        for nutrient_name in common_nutrients:
            nut_total = 0
            for r in recipes:
                nut_total += r.get_nutrient_ratio(nutrient_name).subject_g_per_host_g
            nutrient_ratios[nutrient_name] = model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=nut_total / len(recipes),
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=1,
                    pref_unit='g'
                )
            )

        # Return
        return nutrient_ratios

    def add_recipe(self,
                   recipe_unique_name: str,
                   recipe_qty_data: Optional['model.quantity.QuantityData'] = None
                   ) -> None:
        """Adds a recipe to the meal instance."""
        # Set default for quantity data if none was passed in;
        if recipe_qty_data is None:
            recipe_qty_data = model.quantity.QuantityData(
                quantity_in_g=None,
                pref_unit='g'
            )
        # Add the data to the dict;
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
    def recipe_names(self) -> List[str]:
        """Returns the list of unique recipe names assigned to this instance."""
        recipe_names = []
        for rdf_name in self._meal_data.keys():
            recipe_names.append(model.recipes.get_unique_name_for_datafile_name(rdf_name))
        return recipe_names

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

    def get_recipe_quantity(self,
                            unique_name: Optional[str] = None,
                            df_name: Optional[str] = None
                            ) -> 'model.recipes.ReadonlyRecipeQuantity':
        """Returns the recipe quantity corresponding to the unique name provided."""

        # Raise and exception if we got no params;
        if unique_name is None and df_name is None:
            raise ValueError('Either recipe unique name or datafile name must be specified.')

        # Grab both names;
        if df_name is None:
            df_name = model.recipes.get_datafile_name_for_unique_value(unique_name)
        elif unique_name is None:
            unique_name = model.recipes.get_unique_name_for_datafile_name(df_name)

        # Create and return the recipe quantity instance;
        return model.recipes.ReadonlyRecipeQuantity(
            recipe=model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
                for_unique_name=unique_name
            )),
            quantity_data_src=lambda: self._meal_data[df_name]
        )

    def set_recipe_quantity(self,
                            quantity: float,
                            unit: str,
                            unique_name: Optional[str] = None,
                            df_name: Optional[str] = None,
                            ) -> None:
        """Sets a recipe quantity in arbitrary units."""
        # Figure out the parameters;
        if unique_name is None and df_name is None:
            raise ValueError("Unique name or df name must be specified")
        elif df_name is None:
            df_name = model.recipes.get_datafile_name_for_unique_value(unique_name)

        # Validate the qty and unit;
        quantity = model.quantity.validation.validate_quantity(quantity)
        unit = model.quantity.validation.validate_mass_unit(unit)

        qty_in_g = model.quantity.convert_qty_unit(
            qty=quantity,
            start_unit=unit,
            end_unit='g',
        )

        self._meal_data[df_name] = model.quantity.QuantityData(
            quantity_in_g=qty_in_g,
            pref_unit=unit
        )

    @property
    def recipe_quantities(self) -> Dict[str, 'model.recipes.ReadonlyRecipeQuantity']:
        """Returns the recipe quantities associated with this meal."""
        # Create somewhere to compile the quantities;
        _recipe_quantities = {}

        # Cycle through the meal data and populate the quantities;
        for recipe_df_name, recipe_qty_data in self._meal_data.items():
            _recipe_quantities[recipe_df_name] = self.get_recipe_quantity(df_name=recipe_df_name)

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
