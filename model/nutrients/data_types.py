"""Nutrient module data type definitions."""
from typing import Dict, TypedDict

import model

# Define an alias for nutrient mass data;
NutrientMassData = model.quantity.QuantityData


class NutrientRatioData(TypedDict):
    """Persisted data format for ReadableNutrientRatio instances."""
    nutrient_mass_data: NutrientMassData
    subject_ref_qty_data: model.quantity.QuantityData


# Define a datatype for nutrient ratios data;
NutrientRatiosData = Dict[str, 'NutrientRatioData']
