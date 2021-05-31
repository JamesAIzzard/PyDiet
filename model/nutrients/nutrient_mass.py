"""Defines functionality related to nutrient masses in the model."""
import abc

import model


class NutrientMass(model.quantity.HasQuantityOf, abc.ABC):
    """Base class for readonly and writable nutrient masses."""
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


class ReadonlyNutrientMass(NutrientMass, model.quantity.HasReadonlyQuantityOf):
    """Models a mass of a nutrient."""


class SettableNutrientMass(NutrientMass, model.quantity.HasSettableQuantityOf):
    """Models a settable nutrient mass."""


class HasReadableNutrientMasses(model.quantity.HasQuantityOf, abc.ABC):
    """Models functionality for all classes which have readable nutrient masses."""

    def __init__(self, subject: 'model.nutrients.HasReadableNutrientRatios', **kwargs):
        """Constructor.
        Notes:
            All subjects must have nutrient ratios.
        """
        super().__init__(subject=subject, **kwargs)

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratio's data from the subject ingredient."""
        return self.subject.nutrient_ratios_data

    @property
    def num_calories(self) -> float:
        """Returns the number of calories associated with the instance."""
        return self.subject.calories_per_g * self.quantity_in_g

    def get_nutrient_mass_g(self, nutrient_name: str) -> float:
        """Returns the mass of the named nutrient."""
        return self.subject.get_nutrient_ratio(nutrient_name=nutrient_name).g_per_subject_g * self.quantity_in_g
