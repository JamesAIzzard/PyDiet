"""Defines functionality related to nutrient masses in the model."""
import abc

import model


class NutrientMassBase(model.quantity.IsQuantityOfBase, abc.ABC):
    """Models a mass of a nutrient."""
    def __init__(self, nutrient_name: str, **kwargs):
        super().__init__(
            qty_subject=model.nutrients.GLOBAL_NUTRIENTS[
                model.nutrients.get_nutrient_primary_name(nutrient_name)
            ],
            **kwargs
        )

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        """Returns the nutrient associated with this nutrient mass."""
        return self.qty_subject

    def validate_quantity_and_unit(self) -> None:
        """Extend the validation function to restrict units to masses."""
        super().validate_quantity_and_unit()
        _ = model.quantity.validation.validate_mass_unit(self._unvalidated_qty_pref_unit)


class ReadonlyNutrientMass(NutrientMassBase, model.quantity.IsReadonlyQuantityOf):
    """Models a mass of a nutrient."""


class SettableNutrientMass(NutrientMassBase, model.quantity.IsSettableQuantityOf):
    """Models a settable nutrient mass."""


class HasReadableNutrientMasses(model.quantity.IsQuantityOfBase, abc.ABC):
    """Models functionality for all classes which have readable nutrient masses.
    Note:
        Gotcha here - we don't inherit from HasNutrientRatios becuase it is the *subject*
        that has nutrient ratios, not this QuantityOf instance.
    """

    def __init__(self, **kwargs):
        """Constructor.
        Notes:
            All subjects must have nutrient ratios.
        """
        # Check the qty_subject has nutrient ratios;
        assert(issubclass(kwargs['qty_subject'].__class__, model.nutrients.HasReadableNutrientRatios))

        super().__init__(**kwargs)

    @property
    def nutrient_ratios_data(self) -> 'model.nutrients.NutrientRatiosData':
        """Returns the nutrient ratio's data from the subject ingredient."""
        return self.qty_subject.nutrient_ratios_data

    @property
    def num_calories(self) -> float:
        """Returns the number of calories associated with the instance."""
        return self.qty_subject.calories_per_g * self.quantity_in_g

    def get_nutrient_mass_g(self, nutrient_name: str) -> float:
        """Returns the mass of the named nutrient."""
        return self.qty_subject.get_nutrient_ratio(
            nutrient_name=nutrient_name).subject_g_per_host_g * self.quantity_in_g
