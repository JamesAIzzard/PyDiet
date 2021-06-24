"""Defines recipe quantity classes."""
import abc
from typing import Dict, Callable, Optional, Any

import model
import persistence
from .recipe_ratio import HasReadableRecipeRatios


class RecipeQuantityBase(model.quantity.IsQuantityOfBase, abc.ABC):
    """Base class for recipe quantity classes."""

    def __init__(self, recipe: 'model.recipes.ReadonlyRecipe', **kwargs):
        """Base for recipe quantity classes."""
        # Check the recipe is readonly;
        if not isinstance(recipe, model.recipes.ReadonlyRecipe):
            raise TypeError("Recipe used in quantity must be readonly.")

        # Pass the call on;
        super().__init__(qty_subject=recipe, **kwargs)

    @property
    def recipe(self) -> 'model.recipes.ReadonlyRecipe':
        """Returns the recipe instance.
        Alias for qty_subject."""
        return self.qty_subject


class ReadonlyRecipeQuantity(RecipeQuantityBase, model.quantity.IsReadonlyQuantityOf):
    """Models a readonly recipe quantity."""


class SettableRecipeQuantity(RecipeQuantityBase, model.quantity.IsSettableQuantityOf):
    """Models a settable quantity of."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class HasReadableRecipeQuantities(
    model.ingredients.HasReadableIngredientQuantities,
    HasReadableRecipeRatios,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Mixin class to provide functionality associated with readable recipe quantities."""

    @property
    @abc.abstractmethod
    def recipe_quantities_data(self) -> 'model.recipes.RecipeQuantitiesData':
        """Returns the recipe quantities data for the instance."""
        raise NotImplementedError

    @property
    def recipe_ratios_data(self) -> 'model.recipes.RecipeRatiosData':
        """Returns the recipe ratios data for this instance."""
        rr: Dict[str, 'model.quantity.QuantityRatioData'] = {}
        for rdf_name, r_qd in self.recipe_quantities_data.items():
            rr[rdf_name] = model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=r_qd['quantity_in_g'],
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=self.total_recipes_mass_g,
                    pref_unit='g'
                )
            )
        return rr

    @property
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for this instance."""
        iqd = {}
        for rq in self.recipe_quantities.values():
            for i_uname in rq.recipe.ingredient_unique_names:
                i_df_name = model.ingredients.get_df_name_from_ingredient_name(i_uname)
                if i_df_name not in iqd.keys():
                    iqd[i_df_name] = model.quantity.QuantityData(quantity_in_g=0, pref_unit='g')
                iqd[i_df_name]['quantity_in_g'] += rq.recipe.ingredient_ratios[
                                                       i_df_name].subject_g_per_host_g * rq.quantity_in_g
        return iqd

    @property
    def recipe_quantities(self) -> Dict[str, 'model.recipes.ReadonlyRecipeQuantity']:
        """Returns the readonly recipe quantities for this instance."""
        rqs = {}
        rq_data = self.recipe_quantities_data

        def get_qty_data_src(df_name: str) -> Callable[[], 'model.quantity.QuantityData']:
            """Return accessor function for recipe quantity data."""
            return lambda: self.recipe_quantities_data[df_name]

        for r_df_name, rqd in rq_data.items():
            rqs[r_df_name] = model.recipes.ReadonlyRecipeQuantity(
                recipe=model.recipes.ReadonlyRecipe(
                    recipe_data_src=model.recipes.get_recipe_data_src(for_df_name=r_df_name)
                ),
                quantity_data_src=get_qty_data_src(r_df_name)
            )

        return rqs

    def get_recipe_quantity(self, unique_name: str) -> 'model.recipes.ReadonlyRecipeQuantity':
        """Returns recipe quantity by name."""
        # Get the datafile name;
        rdf_name = model.recipes.get_datafile_name_for_unique_value(unique_name)

        return self.recipe_quantities[rdf_name]

    @property
    def total_recipes_mass_g(self) -> float:
        """Returns the total mass (in g) of the recipes associated with this instance."""
        total = 0
        for rq in self.recipe_quantities_data.values():
            if rq['quantity_in_g'] is not None:
                total += rq['quantity_in_g']
        return total

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for the instance."""
        return self.recipe_quantities_data


class HasSettableRecipeQuantities(HasReadableRecipeQuantities):
    """Mixin to implement functionality associated with settable recipe quantities."""

    def __init__(self, recipe_quantities_data: Optional['model.recipes.RecipeQuantitiesData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._recipe_quantities_data: 'model.recipes.RecipeQuantitiesData' = {}

        if recipe_quantities_data is not None:
            self._recipe_quantities_data = recipe_quantities_data

    @property
    def recipe_quantities_data(self) -> 'model.recipes.RecipeQuantitiesData':
        """Returns the recipe quantities data for this instance."""
        return self._recipe_quantities_data

    def add_recipe(self, recipe_unique_name: str, recipe_qty_data: Optional['model.quantity.QuantityData'] = None):
        """Adds a recipe to the instance."""
        # Get the datafile name;
        recipe_df_name = model.recipes.get_datafile_name_for_unique_value(recipe_unique_name)

        # Raise an exception if its already there;
        if recipe_df_name in self._recipe_quantities_data.keys():
            raise model.recipes.exceptions.RecipeAlreadyAddedError(recipe_unique_name=recipe_unique_name)

        # Put the qty data to default if not provided;
        if recipe_qty_data is None:
            recipe_qty_data = model.quantity.QuantityData(quantity_in_g=None, pref_unit='g')

        # Add it;
        self._recipe_quantities_data[recipe_df_name] = recipe_qty_data

    def set_recipe_quantity(self, recipe_unique_name: str, quantity: float, unit: str) -> None:
        """Sets the quantitiy of a recipe."""
        # Get the datafile name for the recipe;
        rdf_name = model.recipes.get_datafile_name_for_unique_value(recipe_unique_name)

        self._recipe_quantities_data[rdf_name] = model.quantity.QuantityData(
            quantity_in_g=model.quantity.convert_qty_unit(
                qty=quantity,
                start_unit=unit,
                end_unit='g'
            ),
            pref_unit=unit
        )

