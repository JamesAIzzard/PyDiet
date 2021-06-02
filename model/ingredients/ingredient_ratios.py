"""Implements the functionality associated with ingredient ratios."""
import abc

import model
import persistence


class IngredientRatioBase(
    model.quantity.HasRatioOf,
    persistence.YieldsPersistableData,
    abc.ABC
):
    """Abstract base class for readonly and writeable nutrient ratios."""

    @property
    @abc.abstractmethod
    def ingredient_qty(self) -> 'model.ingredients.ReadableIngredientQuantity':
        """Returns the ingredient quantity."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def subject_ref_qty(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the subject reference quantity."""
        raise NotImplementedError

    @property
    def _numerator(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the ratio numerator."""
        return self.ingredient_qty

    @property
    def _denominator(self) -> 'model.quantity.HasReadableQuantityOf':
        """Returns the ratio denominator."""
        return self.subject_ref_qty


class ReadonlyIngredientRatio(IngredientRatioBase):
    """Models a readonly ingredient ratio."""
    pass


class SettableIngredientRatio(IngredientRatioBase):
    """Models a settable ingredient ratio."""
    pass
