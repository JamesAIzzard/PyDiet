import model

# Define an alias for nutrient mass data;
NutrientMassData = model.quantity.QuantityData


class NutrientMass(model.quantity.QuantityOf):
    """Models a mass of a nutrient."""

    def __init__(self, nutrient_name: str, **kwargs):
        # Grab the primary version of the nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        super().__init__(
            subject=model.nutrients.GLOBAL_NUTRIENTS[nutrient_name],
            **kwargs
        )

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        return self._subject


class SettableNutrientMass(NutrientMass, model.quantity.SettableQuantityOf):
    """Models a settable nutrient mass."""
