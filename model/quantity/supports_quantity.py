import abc
from typing import TypedDict, Optional

from model import quantity


class QuantityData(TypedDict):
    quantity_g: Optional[float]
    quantity_units: Optional[str]


class SupportsQuantity(quantity.HasBulk, abc.ABC):
    """Models an amount of substance with mass or volume."""

    def __init__(self, quantity_g: Optional[float] = None, quantity_units: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._quantity_g: Optional[float] = quantity_g
        self._quantity_units: Optional[str] = quantity_units

    @property
    def quantity_g(self) -> Optional[float]:
        """Returns the object's quantity in grams."""
        return self._quantity_g

    @property
    def quantity_units(self) -> Optional[str]:
        """Returns the object's quantity units."""
        return self._quantity_units

    @property
    def quantity_data(self) -> 'QuantityData':
        """Returns a dictionary of the substances quantity data."""
        return QuantityData(quantity_g=self.quantity_g,
                            quantity_units=self.quantity_g)

    @property
    def quantity_is_defined(self) -> bool:
        """Returns True/False to indicate quantity has been defined."""
        return self._quantity_g is not None and self._quantity_units is not None


class SupportsSettableQuantity(SupportsQuantity):
    """Models an amount of substance with a settable mass or volume."""

    def __init__(self):
        super().__init__()

    @SupportsQuantity.quantity_g.setter
    def quantity_g(self, quantity_g: Optional[float]) -> None:
        """Sets the quantity of the instance in g."""
        if quantity_g is None:
            self._quantity_g = None
        else:
            self._quantity_g = quantity.validation.validate_quantity(quantity_g)

    @SupportsQuantity.quantity_units.setter
    def quantity_units(self, units: Optional[str]) -> None:
        """Sets the units of the instance quantity."""
        if units is None:
            self._quantity_units = None
        else:
            if quantity.units_are_volumes(units) and not self.density_is_defined:
                raise quantity.exceptions.DensityNotConfiguredError
            elif quantity.units_are_pieces(units) and not self.piece_mass_defined:
                raise quantity.exceptions.PcMassNotConfiguredError
            else:
                self._quantity_units = quantity.validation.validate_qty_unit(units)

    def set_quantity(self, qty: float, units: str) -> None:
        """Set's the substance's quantity in arbitrary units."""
        units = quantity.validation.validate_qty_unit(units)
        self.quantity_units = units
        self.quantity_g = quantity.convert_qty_unit(qty=qty,
                                                    start_unit=units,
                                                    end_unit='g',
                                                    g_per_ml=self.g_per_ml,
                                                    piece_mass_g=self.piece_mass_g)
