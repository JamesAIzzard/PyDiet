from typing import Optional, TypedDict

import model
import persistence


class NutrientMassData(TypedDict):
    bulk_data: model.quantity.BulkData
    quantity_in_g: Optional[float]


class NutrientMass(model.quantity.HasQuantity, model.SupportsDefinition):
    """Models a measured mass of a nutrient."""

    def __init__(self, nutrient: 'model.nutrients.Nutrient',
                 **kwargs):
        # Since we don't store bulk data on nutrients, we just pass in a dummy
        # HasBulk instance.
        super().__init__(subject=model.quantity.HasBulk(), **kwargs)

        self._nutrient: 'model.nutrients.Nutrient' = nutrient

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        return self._nutrient

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the nutrient mass is defined."""
        return self._get_quantity_in_g() is not None


class SettableNutrientMass(NutrientMass, model.quantity.HasSettableQuantity):
    """Models a settable nutrient mass.
    Notes:
        We don't need to implement load_data or persistable_data, because the only persistable data required
        is already implemented by HasSettableQuantity.
    """

    @model.quantity.HasSettableBulk.pref_unit.setter
    def pref_unit(self, unit: str) -> None:
        # Extend this to limit the pref units to masses;
        super().pref_unit = model.quantity.validation.validate_mass_unit(unit)
