"""Nutrient module data type definitions."""
from typing import Dict

import model


NutrientMassData = model.quantity.QuantityData
NutrientRatiosData = Dict[str, 'model.quantity.RatioData']
