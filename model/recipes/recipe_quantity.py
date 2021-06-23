"""Defines recipe quantity classes."""
import abc
from typing import Dict, Callable, Any

import model
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

    @property
    def total_recipes_mass_g(self) -> float:
        """Returns the total mass (in g) of the recipes associated with this instance."""
        total = 0
        for rq in self.recipe_quantities_data.values():
            total += rq['quantity_in_g']
        return total


class HasSettableRecipeQuantities(
    HasReadableRecipeQuantities,
    abc.ABC
):
    """Mixin to implement functionality associated with settable recipe quantities."""

    @property
    @abc.abstractmethod
    def recipe_quantities_data(self) -> 'model.recipes.RecipeQuantitiesData':
        """Returns the recipe quantities data for this instance."""
        raise NotImplementedError

    @property
    def ingredient_quantities_data(self) -> 'model.ingredients.IngredientQuantitiesData':
        """Returns the ingredient quantities data for this instance."""
        raise NotImplementedError

    @property
    def recipe_quantities(self) -> Dict[str, 'model.recipes.ReadonlyRecipeQuantity']:
        """Returns the recipe quantities associated with this instance."""
        raise NotImplementedError

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the instance's persistable data."""
        raise NotImplementedError
