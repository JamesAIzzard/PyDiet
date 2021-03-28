from typing import Optional

from model import ingredients, recipes, quantity


class RecipeIngredientRatio(quantity.HasSettableQuantity):

    def __init__(self, ingredient: 'ingredients.Ingredient',
                 recipe: 'recipes.Recipe',
                 nominal_quantity: Optional[float],
                 nominal_quantity_units: str,
                 pref_units: Optional[str] = None,
                 perc_incr: Optional[float] = None,
                 perc_decr: Optional[float] = None,
                 **kwargs):
        super().__init__(pref_unit=pref_units, **kwargs)
        self._ingredient = ingredient
        self._recipe = recipe
        self._nominal_quantity_g: Optional[float] = None
        self._perc_incr: Optional[float] = None
        self._perc_decr: Optional[float] = None

        if nominal_quantity is not None and nominal_quantity_units is not None:
            self.set_quantity(qty=nominal_quantity, units=nominal_quantity_units)

        # If we got +/-% then set them.
        # We can use quantity validation to check for percentage incr/decr since
        # a valid quantity has the same constraints.
        if perc_incr is not None:
            self._perc_incr = quantity.validation.validate_quantity(perc_incr)
        if perc_decr is not None:
            self._perc_decr = quantity.validation.validate_quantity(perc_decr)

    def _get_quantity_in_g(self) -> Optional[float]:
        return self._nominal_quantity_g

    def _get_quantity_pref_units(self) -> Optional[str]:
        return self._nominal_quantity_units

    def _set_validated_pref_quantity_units(self, validated_unit: str) -> None:
        self._nominal_quantity_units = validated_unit

    def _set_validated_quantity_in_g(self, validated_quantity_in_g: Optional[float]) -> None:
        self._nominal_quantity_g = validated_quantity_in_g

    @property
    def quantity_in_g(self) -> Optional[float]:
        return self._nominal_quantity_g

    @property
    def quantity_pref_units(self) -> str:
        return self._nominal_quantity_units

    @property
    def perc_incr(self) -> Optional[float]:
        return self._perc_incr

    @property
    def ingredient_name(self) -> Optional[str]:
        """Returns the name of the ingredient."""
        return self._ingredient.name

    @perc_incr.setter
    def perc_incr(self, perc_incr: Optional[float]):
        if perc_incr is None:
            self._perc_incr = None
        else:
            self._perc_incr = quantity.validation.validate_quantity(perc_incr)

    @property
    def perc_decr(self) -> Optional[float]:
        return self._perc_decr

    @perc_decr.setter
    def perc_decr(self, perc_decr: Optional[float]):
        if perc_decr is None:
            self._perc_decr = None
        else:
            self._perc_decr = quantity.validation.validate_quantity(perc_decr)
