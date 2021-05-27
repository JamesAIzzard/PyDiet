"""Defines functionality related to nutrient masses in the model."""
import model

# Define an alias for nutrient mass data;
NutrientMassData = model.quantity.QuantityData


class NutrientMass(model.quantity.QuantityOf):
    """Models a mass of a nutrient."""

    def __init__(self, nutrient_name: str, **kwargs):
        super().__init__(
            subject=model.nutrients.GLOBAL_NUTRIENTS[
                model.nutrients.get_nutrient_primary_name(nutrient_name)
            ],
            **kwargs
        )

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        """Returns the nutrient associated with this nutrient mass."""
        return self._subject


class SettableNutrientMass(model.quantity.SettableQuantityOf):
    """Models a settable nutrient mass."""

    def __init__(self, nutrient_name: str, **kwargs):
        super().__init__(
            subject=model.nutrients.GLOBAL_NUTRIENTS[
                model.nutrients.get_nutrient_primary_name(nutrient_name)
            ],
            **kwargs
        )

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        """Returns the nutrient associated with this nutrient mass."""
        return self._subject
