"""Defines data types for the ingredients module."""
from typing import Optional, Dict, TypedDict

import model


class IngredientData(TypedDict):
    """Ingredient data dictionary."""
    cost_per_qty_data: model.cost.CostPerQtyData
    flag_data: model.flags.FlagDOFData
    name: Optional[str]
    nutrient_ratios_data: model.nutrients.NutrientRatiosData
    extended_units_data: model.quantity.ExtendedUnitsData


IngredientQuantitiesData = Dict[str, model.quantity.QuantityData]


class IngredientRatioData(TypedDict):
    """Ingredient ratio data dictionary."""
    subject_qty_data: model.quantity.QuantityData
    host_qty_data: model.quantity.QuantityData


IngredientRatiosData = Dict[str, model.quantity.QuantityRatioData]
