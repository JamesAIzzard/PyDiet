"""Defines data types relating to the recipe module."""
from typing import List, Dict, TypedDict, Optional

import model


class RecipeData(TypedDict):
    """Recipe data dictionary."""
    name: Optional[str]
    ingredient_quantities_data: model.ingredients.IngredientQuantitiesData
    serve_intervals: List[str]
    instruction_src: Optional[str]
    tags: List[str]


RecipeRatiosData = Dict[str, model.quantity.QuantityRatioData]
RecipeQuantitiesData = Dict[str, model.quantity.QuantityData]
