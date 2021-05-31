"""Defines the data types for the cost module."""
from typing import Optional

import model


class CostPerQtyData(model.quantity.QuantityData):
    """Cost data persistence format."""
    cost_per_g: Optional[float]
