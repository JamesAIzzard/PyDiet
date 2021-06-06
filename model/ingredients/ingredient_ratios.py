"""Implements the functionality associated with ingredient ratios."""
import abc

import model
import persistence


class IngredientRatioBase(
    model.quantity.IsQuantityRatioBase,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Abstract base class for readonly and writeable nutrient ratios."""


class ReadonlyIngredientRatio(IngredientRatioBase, model.quantity.IsReadonlyQuantityRatio):
    """Models a readonly ingredient ratio."""


class SettableIngredientRatio(IngredientRatioBase, model.quantity.IsSettableQuantityRatio):
    """Models a settable ingredient ratio."""
    pass
