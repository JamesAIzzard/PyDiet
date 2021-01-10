import abc
from typing import TypedDict, Optional

from pydiet import quantity
from pydiet.quantity import HasBulk, exceptions, validation


class QuantityData(TypedDict):
    qty_g: Optional[float]
    qty_units: Optional[str]


class SupportsQuantity(HasBulk, abc.ABC):
    """Models an amount of substance with mass or volume."""

    def __init__(self, qty_g: Optional[float] = None, qty_units: Optional[str] = None, **kwargs):
        self._qty_g: Optional[float] = qty_g
        self._qty_units: Optional[str] = qty_units
        super().__init__(**kwargs)

    @property
    def qty_g(self) -> Optional[float]:
        """Returns the object's qty in grams."""
        return self._qty_g

    def _set_qty_g(self, qty_g: Optional[float]) -> None:
        """Implementation to set the substance quantity in grams."""
        raise exceptions.QuantityNotSettableError

    @qty_g.setter
    def qty_g(self, qty_g: Optional[float]) -> None:
        """Sets the quantity of the substance in grams."""
        self._set_qty_g(qty_g)

    @property
    def qty_units(self) -> Optional[str]:
        """Returns the object's quantity units."""
        return self._qty_units

    def _set_qty_units(self, units: Optional[str]) -> None:
        """Implementation to sets the units for the object's quantity"""
        raise exceptions.QuantityNotSettableError

    @qty_units.setter
    def qty_units(self, units: Optional[str]) -> None:
        """Sets the units for the quantity of the object."""
        self._set_qty_units(units)

    @property
    def quantity_data(self) -> 'QuantityData':
        """Returns a dictionary of the substances quantity data."""
        return QuantityData(qty_g=self.qty_g,
                            qty_units=self.qty_g)

    @property
    def quantity_is_defined(self) -> bool:
        """Returns True/False to indicate quantity has been defined."""
        return self._qty_g is not None and self._qty_units is not None


class SupportsSettableQuantity(SupportsQuantity):
    """Models an amount of substance with a settable mass or volume."""

    def _set_qty_g(self, qty_g: Optional[float]) -> None:
        """Implements setting for substance quantity in grams."""
        if qty_g is None:
            self._qty_g = None
        else:
            self._qty_g = validation.validate_quantity(qty_g)

    def _set_qty_units(self, units: Optional[str]) -> None:
        """Implements setting for the substance qty units."""
        if units is None:
            self._qty_units = None
        else:
            if quantity.units_are_volumes(units) and not self.density_is_defined:
                raise exceptions.DensityNotConfiguredError
            elif quantity.units_are_pieces(units) and not self.piece_mass_defined:
                raise exceptions.PcMassNotConfiguredError
            else:
                self._qty_units = validation.validate_qty_unit(units)

    def set_quantity(self, qty: float, units: str) -> None:
        """Set's the substance's quantity in arbitrary units."""
        units = validation.validate_qty_unit(units)
        self.qty_units = units
        self.qty_g = quantity.convert_qty_unit(qty=qty,
                                               start_unit=units,
                                               end_unit='g',
                                               g_per_ml=self.g_per_ml,
                                               piece_mass_g=self.piece_mass_g)
