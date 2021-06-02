"""Defines the custom data types used with the quantity module."""
from typing import TypedDict, Optional


class ExtendedUnitsData(TypedDict):
    """Persistable data format for the extended units class."""
    g_per_ml: Optional[float]
    piece_mass_g: Optional[float]


class QuantityData(TypedDict):
    """Persistable data format for modelling quantities of substances."""
    quantity_in_g: Optional[float]
    pref_unit: str
