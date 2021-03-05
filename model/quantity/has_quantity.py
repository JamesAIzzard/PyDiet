import abc
from typing import TypedDict, Optional

from model import quantity


class QuantityData(TypedDict):
    quantity_in_g: Optional[float]
    quantity_units: Optional[str]


class HasQuantity(quantity.HasBulk, abc.ABC):
    """Models a quantity of substance with mass or volume."""

    def __init__(self, **kwargs):
        """Don't initialise values here because different child classes will implement
        these values in different ways."""
        super().__init__(**kwargs)

    @property
    @abc.abstractmethod
    def quantity_in_g(self) -> Optional[float]:
        """Returns the object's quantity in grams."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def quantity_pref_units(self) -> Optional[str]:
        """Returns the object's quantity units."""
        raise NotImplementedError

    @property
    def quantity_is_defined(self) -> bool:
        """Returns True/False to indicate quantity has been defined."""
        return self.quantity_in_g is not None and self.quantity_pref_units is not None


class HasSettableQuantity(HasQuantity):
    """Models a quantity of substance with a settable mass or volume."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abc.abstractmethod
    def _set_validated_pref_quantity_units(self, validated_unit: str) -> None:
        """Sets the validated quantity units on the instance."""
        raise NotImplementedError

    @abc.abstractmethod
    def _set_validated_quantity_in_g(self, validated_quantity_in_g: Optional[float]) -> None:
        """Sets the validated quantity in grams on the instance."""

    @HasQuantity.quantity_in_g.setter
    def quantity_in_g(self, quantity_g: Optional[float]) -> None:
        """Sets the quantity of the instance in g."""
        if quantity is not None:
            quantity_g = quantity.validation.validate_quantity(quantity_g)
        self._set_validated_quantity_in_g(quantity_g)

    @HasQuantity.quantity_pref_units.setter
    def quantity_pref_units(self, units: str) -> None:
        """Sets the units of the instance quantity."""
        if quantity.units_are_volumes(units) and not self.density_is_defined:
            raise quantity.exceptions.DensityNotConfiguredError
        elif quantity.units_are_pieces(units) and not self.piece_mass_defined:
            raise quantity.exceptions.PcMassNotConfiguredError
        else:
            self._set_validated_quantity_pref_units(quantity.validation.validate_qty_unit(units))

    def set_quantity(self, qty: float, units: str) -> None:
        """Set's the substance's quantity in arbitrary units."""
        units = quantity.validation.validate_qty_unit(units)
        self.quantity_pref_units = units
        self.quantity_in_g = quantity.convert_qty_unit(qty=qty,
                                                       start_unit=units,
                                                       end_unit='g',
                                                       g_per_ml=self.g_per_ml,
                                                       piece_mass_g=self.piece_mass_g)
