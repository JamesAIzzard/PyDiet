"""Defines meal classes."""
from typing import Dict, Optional, Any

import model
import persistence


class SettableMeal(
    model.recipes.HasSettableRecipeQuantities,
    persistence.YieldsPersistableData,
):
    """Models a collection of recipes (combined to form a meal)."""

    def __init__(self, meal_data: Optional['model.meals.MealData'] = None, **kwargs):
        super().__init__(recipe_quantities_data=meal_data, **kwargs)

    @property
    def pricetag(self) -> float:
        """Use the fast pre-cache data to determine the price of each meal."""
        total_cost = 0
        for rec_dfn, rec_df in self.recipe_quantities_data.items():
            cost_per_g = persistence.get_precalc_data_for_recipe(rec_dfn)['cost_per_qty_data']['cost_per_g']
            total_cost += cost_per_g * rec_df['quantity_in_g']
        return total_cost

    @property
    def num_calories(self) -> float:
        """Use the fast pre-cache data to get the number of calories."""
        total_cals = 0
        for rec_dfn, rec_df in self.recipe_quantities_data.items():
            cals_per_g = persistence.get_precalc_data_for_recipe(rec_dfn)['calories_per_g']
            total_cals += cals_per_g * rec_df['quantity_in_g']
        return total_cals

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Shortcut the inheritence tree to deliver these faster if the cache is available."""
        try:
            nrd = {}
            for rec_dfn, rrd in self.recipe_ratios_data.items():
                rec_precalc_data = persistence.get_precalc_data_for_recipe(rec_dfn)['nutrient_ratios_data']
                for nut_name, nut_ratio_data in rec_precalc_data.items():
                    if nut_name not in nrd:
                        nrd[nut_name] = model.quantity.QuantityRatioData(
                            subject_qty_data=model.quantity.QuantityData(quantity_in_g=0, pref_unit='g'),
                            host_qty_data=model.quantity.QuantityData(quantity_in_g=1, pref_unit='g')
                        )
                    nrd[nut_name]['subject_qty_data']['quantity_in_g'] += model.quantity.get_ratio_from_qty_ratio_data(
                        nut_ratio_data) * model.quantity.get_ratio_from_qty_ratio_data(rrd)
            return nrd
        except KeyError:
            # Cache not available, do it the long way;
            return super().nutrient_ratios_data

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns the persistable data for this meal instance."""
        return self._recipe_quantities_data
