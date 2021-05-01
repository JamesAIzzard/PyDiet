import abc
from typing import Dict, TypedDict, Optional, Any

import model
import persistence


class QuantityData(TypedDict):
    quantity_in_g: Optional[float]
    quantity_pref_unit: str


class HasQuantity(abc.ABC):
    """Models a quantity of substance with mass or volume.
    Notes:
        We don't store the values on this class, because some implementations, such as RecipeQuantity
        will derive their quantity information from the IngredientQuantities stored against it.

        I did consider adding SupportsDefinition as a parent class, but it seems too much. Lots of things
        are going to subclass this, and its not clear to me they will always support the concept of
        being defined.
    """

    def __init__(self, subject: 'model.quantity.HasBulk', **kwargs):
        super().__init__(**kwargs)
        self._subject = subject

    @abc.abstractmethod
    def _get_quantity_in_g(self) -> Optional[float]:
        """Implements the way the concrete class stores/retrieves the quantity in grams"""
        raise NotImplementedError

    @abc.abstractmethod
    def _get_quantity_pref_unit(self) -> str:
        """Implements they quantity pref unit retrival on the concrete class."""
        raise NotImplementedError

    @property
    def quantity_in_g(self) -> float:
        """Returns the object's quantity in grams."""
        if self._get_quantity_in_g() is None:
            raise model.quantity.exceptions.UndefinedQuantityError()
        else:
            return self._get_quantity_in_g()

    @property
    def quantity_pref_unit(self) -> str:
        """Returns the subject's preferred unit."""
        return self._get_quantity_pref_unit()

    @property
    def quantity_in_pref_units(self) -> float:
        """Returns the isntance's quantity in its preferred units."""
        return model.quantity.convert_qty_unit(
            qty=self.quantity_in_g,
            start_unit='g',
            end_unit=self.quantity_pref_unit,
            g_per_ml=self._subject.g_per_ml if self._subject.density_is_defined else None,
            piece_mass_g=self._subject.piece_mass_g if self._subject.piece_mass_defined else None
        )


class HasSettableQuantity(HasQuantity, persistence.HasPersistableData):
    """Models a quantity of substance with a settable mass or volume.
    Notes:
        Since the quantity is settable on this instance, it is safe to assume the values
        are stored on this instance. It also means we can export the persistable data from this
        instance, hence we inherit HasPersistableData.
    """

    def __init__(self, quantity_data: Optional['QuantityData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._quantity_in_g = None
        self._quantity_pref_unit = 'g'

        if quantity_data is not None:
            self.load_data(quantity_data)

    def _get_quantity_in_g(self) -> Optional[float]:
        return self._quantity_in_g

    @HasQuantity.quantity_in_g.setter
    def quantity_in_g(self, value: Optional[float]) -> None:
        """Sets the quantity of the instance in g."""
        if value is None:
            self._quantity_in_g = None
        else:
            value = model.quantity.validation.validate_quantity(value)
            self._quantity_in_g = value

    def _get_quantity_pref_unit(self) -> str:
        return self._quantity_pref_unit

    @HasQuantity.quantity_pref_unit.setter
    def quantity_pref_unit(self, unit: str) -> None:
        """Sets the quantity pref unit."""
        # First, validate the unit;
        unit = model.quantity.validation.validate_qty_unit(unit)
        # Only allow a volume unit if the subject's density is configured;
        if model.quantity.units_are_volumes(unit):
            if not self._subject.density_is_defined:
                raise model.quantity.exceptions.UndefinedDensityError(subject=self)
        elif model.quantity.units_are_pieces(unit):
            if not self._subject.piece_mass_defined:
                raise model.quantity.exceptions.UndefinedPcMassError(subject=self)
        # No issues, go ahead and set;
        self._quantity_pref_unit = unit

    def set_quantity(self, qty: float, unit: str) -> None:
        """Set's the substance's quantity in arbitrary units."""
        # Convert the value into grams;
        quantity_in_g = model.quantity.convert_qty_unit(
            qty=qty,
            start_unit=unit,
            end_unit='g',
            g_per_ml=self._subject.g_per_ml if self._subject.density_is_defined else None,
            piece_mass_g=self._subject.piece_mass_g if self._subject.piece_mass_defined else None
        )

        # Set the values;
        self.quantity_in_g = quantity_in_g
        self.quantity_pref_unit = unit

    def load_data(self, data: 'QuantityData') -> None:
        super().load_data(data)
        self.quantity_in_g = data['quantity_in_g']
        # To repair data which does't have the pref unit considered, we'll revert to grams if
        # the unit isn't configured on the subject;
        if not self._subject.units_are_configured(data['quantity_pref_unit']):
            self.quantity_pref_unit = 'g'
        else:
            self.quantity_pref_unit = data['quantity_pref_unit']

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Just put in the quantity data here. Don't put in the subject's bulk data,
        that will be saved in the subject's datafile, so we don't want to duplicate it."""
        data = super().persistable_data
        data['quantity_in_g'] = self._quantity_in_g
        data['quantity_pref_unit'] = self._quantity_pref_unit
        return data
