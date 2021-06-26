"""Implements the functionality associated with ingredient ratios."""
import abc
from typing import List, Dict, Optional

import model
import persistence


class IngredientRatioBase(
    model.quantity.IsQuantityRatioBase,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Abstract base class for readonly and writeable nutrient ratios."""

    def __init__(self, ingredient: 'model.ingredients.IngredientBase', **kwargs):
        if not isinstance(ingredient, model.ingredients.IngredientBase):
            raise TypeError("Ingredient must be an subclass of IngredientBase.")

        super().__init__(ratio_subject=ingredient, **kwargs)

    @property
    def ingredient(self) -> 'model.ingredients.ReadonlyIngredient':
        """Returns the ingredient associated with the ratio."""
        return self._ratio_subject


class ReadonlyIngredientRatio(IngredientRatioBase, model.quantity.IsReadonlyQuantityRatio):
    """Models a readonly ingredient ratio."""


class HasReadableIngredientRatios(
    model.cost.HasReadableCostPerQuantity,
    model.flags.HasReadableFlags,
    model.nutrients.HasReadableNutrientRatios,
    abc.ABC
):
    """Mixin to implement functionality associated with having readable ingredient ratios."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cache the ingredient ratios;
        self._ingredient_ratios = {}

    @property
    @abc.abstractmethod
    def ingredient_ratios_data(self) -> 'model.ingredients.IngredientRatiosData':
        """Returns the ingredient ratios data associated with this instance."""
        raise NotImplementedError

    @property
    def flag_dofs(self) -> 'model.flags.FlagDOFData':
        """Returns a dictionary of each non-direct alias flag."""
        _flag_dofs = {}
        for flag in model.flags.ALL_FLAGS.values():
            if not flag.direct_alias:
                _flag_dofs[flag.name] = True
        for ir in self.ingredient_ratios.values():
            for fn in _flag_dofs.keys():
                if ir.ingredient.flag_dofs[fn] is False:
                    _flag_dofs[fn] = False
                elif ir.ingredient.flag_dofs[fn] is None:
                    _flag_dofs[fn] = None
        return _flag_dofs

    @property
    def cost_per_qty_data(self) -> 'model.cost.CostPerQtyData':
        """Returns the cost_per_qty data for the instance."""
        cpg = 0
        for ir in self.ingredient_ratios.values():
            cpg += ir.ingredient.cost_per_g * ir.subject_g_per_host_g
        return model.cost.CostPerQtyData(
            quantity_in_g=100,
            pref_unit='g',
            cost_per_g=cpg
        )

    @property
    def ingredient_ratios(self) -> Dict[str, 'ReadonlyIngredientRatio']:
        """Returns the ingredient ratio instances associated with this instance."""

        # Create a dict to compile the ratios;
        irs: Dict[str, 'ReadonlyIngredientRatio'] = {}

        # Create somewhere to compile the total to catch >1 error;
        total_ratio_float = 0

        # Compile the ratios;
        for idf_name, ratio_data in self.ingredient_ratios_data.items():
            irs[idf_name] = self.get_ingredient_ratio(
                ingredient_df_name=idf_name
            )
            total_ratio_float += irs[idf_name].subject_g_per_host_g

        # Check for >1 error;
        if total_ratio_float > 1.0001:
            raise model.ingredients.exceptions.IngredientRatiosSumExceedsOneError()

        return irs

    def get_ingredient_ratio(
            self,
            ingredient_unique_name: Optional[str] = None,
            ingredient_df_name: Optional[str] = None
    ) -> 'ReadonlyIngredientRatio':
        """Returns an ingredient ratio by name."""
        # Handle the arguments;
        if ingredient_df_name is None and ingredient_unique_name is None:
            raise ValueError("Either ingredient unique name or df name must be provided.")
        elif ingredient_df_name is None:
            ingredient_df_name = model.ingredients.get_df_name_from_ingredient_name(ingredient_unique_name)

        if ingredient_df_name in self._ingredient_ratios.keys():
            return self._ingredient_ratios[ingredient_df_name]

        # Create and return the instance;
        self._ingredient_ratios[ingredient_df_name] = ReadonlyIngredientRatio(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=model.ingredients.get_ingredient_data_src(
                    for_df_name=ingredient_df_name
                )
            ),
            ratio_host=self,
            qty_ratio_data_src=lambda: self.ingredient_ratios_data[ingredient_df_name]
        )
        return self._ingredient_ratios[ingredient_df_name]

    @property
    def ingredient_unique_names(self) -> List[str]:
        """Returns a list of the ingredient names associated with the instance."""
        names: List[str] = []

        for ingredient_df_name in self.ingredient_ratios_data.keys():
            names.append(model.ingredients.get_ingredient_name_from_df_name(ingredient_df_name))

        return names

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratios data for the instance."""

        # Create somewhere to cache the ingredient ratios;
        ingredient_ratio_cache = self.ingredient_ratios

        # Figure out which set of nutrients is defined on every ingredient;
        defined_nutrient_sets = []
        # Cycle through each ingredient;
        for ir in ingredient_ratio_cache.values():
            # Collect its nutrient ratio names;
            defined_nutrient_sets.append(set(ir.ingredient.defined_nutrient_ratio_names))
        # Grab the intersection of defined nutrient sets;
        if len(defined_nutrient_sets) > 0:
            common_nutrients = set.intersection(*defined_nutrient_sets)
        else:
            common_nutrients = []

        # Now work out the nutrient ratios for the recipe;
        nutrient_ratios: 'model.nutrients.NutrientRatiosData' = {}
        nutrient_ratio_floats: Dict[str, float] = {nutr_name: 0 for nutr_name in common_nutrients}

        # Now cycle through each ingredient, and use it to contribute its nutrient ratio based on its ratio;
        for ir in ingredient_ratio_cache.values():
            for nutrient_name in common_nutrients:
                nutrient_ratio_floats[nutrient_name] += ir.ingredient.get_nutrient_ratio(
                    nutrient_name).subject_g_per_host_g * ir.subject_g_per_host_g
        # Now convert the float dict to a nutrient ratio dict;
        for nutrient_name in nutrient_ratio_floats.keys():
            nutrient_ratios[nutrient_name] = model.quantity.QuantityRatioData(
                subject_qty_data=model.quantity.QuantityData(
                    quantity_in_g=nutrient_ratio_floats[nutrient_name],
                    pref_unit='g'
                ),
                host_qty_data=model.quantity.QuantityData(
                    quantity_in_g=1, pref_unit='g'
                )
            )

        # Return
        return nutrient_ratios
