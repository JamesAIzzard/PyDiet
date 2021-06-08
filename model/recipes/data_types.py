"""Defines data types relating to the recipe module."""
from typing import List, Dict, TypedDict, Optional

import model


class RecipeData(TypedDict):
    """Recipe data dictionary."""
    name: Optional[str]
    ingredient_quantities_data: Dict[str, 'model.ingredients.IngredientQuantitiesData']
    serve_intervals: List[str]
    instruction_src: str
    tags: List[str]
