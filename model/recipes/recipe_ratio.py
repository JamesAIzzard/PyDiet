"""Defines classes modelling recipe ratio functionality."""
import abc
from typing import Dict, List, Optional

import model
import persistence


class RecipeRatioBase(
    model.quantity.IsQuantityRatioBase,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Abstract base class for readonly and writable recipe ratios."""

    def __init__(self, recipe: 'model.recipes.ReadonlyRecipe', **kwargs):
        # Check the recipe is a ReadonlyRecipe;
        if not isinstance(recipe, model.recipes.ReadonlyRecipe):
            raise TypeError("Recipe arg must be a ReadonlyRecipe instance.")

        # Pass recipe on to quantity class;
        super().__init__(ratio_subject=recipe, **kwargs)

    @property
    def recipe(self) -> 'model.recipes.ReadonlyRecipe':
        """Returns the recipe associated with this recipe ratio."""
        return self._ratio_subject


class ReadonlyRecipeRatio(RecipeRatioBase, model.quantity.IsReadonlyQuantityRatio):
    """Models a readonly recipe ratio."""


class SettableRecipeRatio(RecipeRatioBase, model.quantity.IsSettableQuantityRatio):
    """Models a readable recipe ratio."""


class HasReadableRecipeRatios(
    model.ingredients.HasReadableIngredientRatios,
    abc.ABC
):
    """Mixin to implement functionality associated with having recipe ratios."""

    @property
    @abc.abstractmethod
    def recipe_ratios_data(self) -> 'model.recipes.RecipeRatiosData':
        """Returns the recipe ratios associated with this instance."""
        raise NotImplementedError

    @property
    def recipes(self) -> Dict[str, 'model.recipes.ReadonlyRecipe']:
        """Returns dict of readonly recipes associated with the instnace."""
        rps = {}
        for rec_name in self.recipe_ratios_data.keys():
            rps[rec_name] = model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(
                for_df_name=rec_name
            ))
        return rps

    @property
    def ingredient_ratios_data(self) -> 'model.ingredients.IngredientRatiosData':
        """Returns the ingredient ratios data associated with this instance."""
        # Create a scratch file to store the ratios as floats. We can convert these to ratio objects
        # later on.
        irs_scratch: Dict[str, float] = {}

        # Now cycle through, and calculate the ratios;
        for recipe_ratio in self.recipe_ratios.values():
            for idf_name, ingredient_ratio in recipe_ratio.recipe.ingredient_ratios.items():
                if idf_name not in irs_scratch:
                    irs_scratch[idf_name] = 0
                irs_scratch[idf_name] += recipe_ratio.subject_g_per_host_g * ingredient_ratio.subject_g_per_host_g

        # Now convert the float ratios into proper ratio instances;
        irs: Dict[str, model.quantity.QuantityRatioData] = {}
        for idf_name, float_ratio in irs_scratch.items():
            irs[idf_name] = model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=float_ratio * 100,
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=100,
                    pref_unit='g'
                )
            )

        # Return the ingredient ratios data;
        return irs

    def get_recipe_ratio(self, unique_name: Optional[str] = None,
                         df_name: Optional[str] = None) -> 'ReadonlyRecipeRatio':
        """Returns the a readonly recipe ratio to represent the named recipe instance."""
        if unique_name is None and df_name is None:
            raise ValueError("Either df_name or unique_name must be specified.")
        if df_name is None:
            df_name = model.recipes.get_datafile_name_for_unique_value(unique_name)

        return model.recipes.ReadonlyRecipeRatio(
            recipe=model.recipes.ReadonlyRecipe(recipe_data_src=model.recipes.get_recipe_data_src(for_df_name=df_name)),
            ratio_host=self,
            qty_ratio_data_src=lambda: self.recipe_ratios_data[df_name]
        )

    @property
    def recipe_ratios(self) -> Dict[str, ReadonlyRecipeRatio]:
        """Returns a list of readonly recipe ratios associated with this instance."""
        rr = {}
        for rec_df_name in self.recipe_ratios_data.keys():
            rr[rec_df_name] = self.get_recipe_ratio(df_name=rec_df_name)
        return rr

    @property
    def unique_recipe_names(self) -> List[str]:
        """Returns the list of unique recipe names associated with this meal."""
        runs: List[str] = []
        for rec_df_name in self.recipe_ratios_data.keys():
            runs.append(model.recipes.get_unique_name_for_datafile_name(rec_df_name))
        return runs
