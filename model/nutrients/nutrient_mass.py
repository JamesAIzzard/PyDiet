from typing import Optional, Dict, TypedDict, Any

import model
import persistence


class NutrientMassData(TypedDict):
    bulk_data: model.quantity.BulkData
    quantity_in_g: Optional[float]


class NutrientMass(model.quantity.HasQuantity, model.SupportsDefinition, persistence.HasPersistableData):
    """Models a measured mass of a nutrient.
    Notes:
        HasQuantity doesn't naturally store data on the instance, but we want this
        readonly Nutrient mass class to store its data. So we init the quantity data dict.
    """

    def __init__(self, nutrient: 'model.nutrients.Nutrient',
                 nutrient_mass_data: Optional['NutrientMassData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._nutrient: 'model.nutrients.Nutrient' = nutrient
        self._quantity_in_g: Optional[float] = None

        if nutrient_mass_data is not None:
            self.load_data(data=nutrient_mass_data)

    def _get_quantity_in_g(self) -> Optional[float]:
        return self._quantity_in_g

    @property
    def nutrient(self) -> 'model.nutrients.Nutrient':
        return self._nutrient

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the nutrient mass is defined."""
        return self._quantity_in_g is not None

    def load_data(self, data: 'NutrientMassData', **kwargs) -> None:
        super().load_data(data)
        # Restrict the units to masses;
        model.quantity.validation.validate_mass_unit(data['bulk_data']['pref_unit'])
        # Load the data as normal;
        self._quantity_in_g = data['quantity_in_g']

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        data['quantity_in_g'] = self._quantity_in_g
        return data


class SettableNutrientMass(NutrientMass, model.quantity.HasSettableQuantity):
    """Models a settable nutrient mass."""

    @model.quantity.HasSettableBulk.pref_unit.setter
    def pref_unit(self, unit: str) -> None:
        # Extend this to limit the pref units to masses;
        super().pref_unit = model.quantity.validation.validate_mass_unit(unit)
