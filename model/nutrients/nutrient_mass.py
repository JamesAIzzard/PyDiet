from typing import Optional

import model
import persistence


class NutrientMass(model.quantity.HasQuantityOf, model.SupportsDefinition, persistence.CanLoadData):
    """Models a mass of a nutrient."""

    def __init__(self, nutrient: 'model.nutrients.Nutrient',
                 mass_data: Optional['model.quantity.QuantityData'] = None,
                 **kwargs):
        super().__init__(subject=nutrient, **kwargs)

        self._quantity_data_ = model.quantity.QuantityData(
            quantity_in_g=None,
            pref_unit='g'
        )

        if mass_data is not None:
            self.load_data(mass_data)

    @property
    def _quantity_data(self) -> 'model.quantity.QuantityData':
        return self._quantity_data_

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        return self._subject

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the nutrient mass is defined."""
        return self._quantity_data_['quantity_in_g'] is not None

    def load_data(self, data: 'model.quantity.QuantityData') -> None:
        self._quantity_data_ = data


class SettableNutrientMass(NutrientMass, model.quantity.HasSettableQuantityOf):
    """Models a settable nutrient mass."""
