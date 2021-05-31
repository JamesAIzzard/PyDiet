"""Defines enumeration class to indicate implication of a flag on a nutrient."""
import enum


class FlagImpliesNutrient(enum.Enum):
    """Enumeration to describe the implication of a flag on a nutrient mass."""
    zero = 1
    non_zero = 2
