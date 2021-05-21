"""Ingredient functionality module."""
from typing import Optional, TypedDict

import model
import persistence


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_qty_data: model.cost.CostPerQtyData
    flag_data: model.flags.FlagDOFData
    name: Optional[str]
    nutrient_ratios_data: model.nutrients.NutrientRatiosData
    extended_units_data: model.quantity.ExtendedUnitsData


class Ingredient(
    persistence.SupportsPersistence,
    model.HasName
):
    """Readonly ingredient model."""

    def __init__(self, unique_name: Optional[str] = None, df_name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        # Raise an exception if no info was provided;
        if unique_name is None and df_name is None:
            raise ValueError("Either unique name or datafile name must be provided to init an Ingredient.")

        self._unique_name = unique_name
        self._df_name = df_name

    @staticmethod
    def get_path_into_db() -> str:
        """Returns the path into the ingredient database."""
        return f"{persistence.configs.path_into_db}/ingredients"

    @property
    def unique_value(self) -> str:
        """Returns the ingredient's unique name."""
        return self.name
