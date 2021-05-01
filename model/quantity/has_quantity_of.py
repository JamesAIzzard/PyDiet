import abc
from typing import Dict, TypedDict, Optional, Any

import model
import persistence


class QuantityData(TypedDict):
    quantity_in_g: Optional[float]
    pref_unit: str


class HasQuantityOf(persistence.YieldsPersistableData, abc.ABC):
    """Models a quantity of substance with mass or volume. Examples of classes that will
    sublcass this include NutrientMass, RecipeQuantity and IngredientQuantity.
    Notes:
        I did consider adding SupportsDefinition as a parent class, but it seems too much. Lots of things
        are going to subclass this, and its not clear to me they will always support the concept of
        being defined.
    """

    def __init__(self, subject: Any, **kwargs):
        super().__init__(**kwargs)

        self._subject = subject

    @property
    @abc.abstractmethod
    def _quantity_data(self) -> 'QuantityData':
        """Subclass implementation to retrieve quantity data for the instance."""
        raise NotImplementedError

    @property
    def quantity_in_g(self) -> float:
        """Returns the object's quantity in grams."""
        if self._quantity_data['quantity_in_g'] is None:
            raise model.quantity.exceptions.UndefinedQuantityError()
        else:
            return self._quantity_data['quantity_in_g']

    def _reset_pref_unit(self) -> None:
        self._quantity_data['pref_unit'] = 'g'

    def _sanitise_pref_unit(self) -> None:
        try:
            _ = self._validate_pref_unit(self._quantity_data['pref_unit'])
        except (
                model.quantity.exceptions.UnknownUnitError,
                model.quantity.exceptions.UnitNotConfiguredError
        ):
            self._reset_pref_unit()

    def _validate_pref_unit(self, unit: str) -> str:
        # If the unit isn't recognised, just replace it with grams
        unit = model.quantity.validation.validate_qty_unit(unit)

        # If the subject doesn't support extended units;
        if not isinstance(self._subject, model.quantity.SupportsExtendedUnits):
            # If the unit is a volume, raise the volume exception;
            if model.quantity.units_are_volumes(unit):
                raise model.quantity.exceptions.UndefinedDensityError(subject=self)
            # If the unit is a pc, raise the pc exception;
            if model.quantity.units_are_pieces(unit):
                raise model.quantity.exceptions.UndefinedPcMassError(subject=self)

        # OK, so the subject does support extended units;
        # If the unit is a volume, and the subject doesn't have density defined;
        if model.quantity.units_are_volumes(unit) and not self._subject.density_is_defined:
            raise model.quantity.exceptions.UndefinedDensityError(subject=self)
        elif model.quantity.units_are_pieces(unit) and not self._subject.piece_mass_defined:
            raise model.quantity.exceptions.UndefinedPcMassError(subject=self)

        # OK, return the unit;
        return unit

    @property
    def quantity_pref_unit(self) -> str:
        """Returns the unit used to define the subject quantity.
        Notes:
            By sanitising the pref unit, we can stop this class returning
            units that are not configured on the subject.
        """
        self._sanitise_pref_unit()
        return self._quantity_data['pref_unit']

    @property
    def quantity_in_pref_units(self) -> float:
        """Returns the isntance's quantity in its preferred units."""
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self._subject, model.quantity.SupportsExtendedUnits):
            g_per_ml = self._subject.g_per_ml if self._subject.density_is_defined else None
            piece_mass_g = self._subject.piece_mass_g if self._subject.piece_mass_defined else None
        return model.quantity.convert_qty_unit(
            qty=self.quantity_in_g,
            start_unit='g',
            end_unit=self.quantity_pref_unit,
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )

    @property
    def persistable_data(self) -> Dict[str, Any]:
        data = super().persistable_data
        self._sanitise_pref_unit()
        data['quantity_data'] = self._quantity_data
        return data


class HasSettableQuantityOf(HasQuantityOf, persistence.CanLoadData):
    """Models a settable quantity of a substance."""

    def __init__(self, quantity_data: Optional['QuantityData'] = None, **kwargs):
        # We are now storing the quantity data locally to this instance, so wire the retrieval
        # callbacks up to the new instance variables;
        super().__init__(**kwargs)

        self._quantity_data_: 'model.quantity.QuantityData' = QuantityData(
            quantity_in_g=None,
            pref_unit='g'
        )

        if quantity_data is not None:
            self.load_data(quantity_data)

    @property
    def _quantity_data(self) -> 'QuantityData':
        return self._quantity_data_

    @HasQuantityOf.quantity_in_g.setter
    def quantity_in_g(self, value: Optional[float]) -> None:
        """Sets the quantity of the instance in g."""
        if value is None:
            self._quantity_data['quantity_in_g'] = None
        else:
            self._quantity_data['quantity_in_g'] = model.quantity.validation.validate_quantity(value)

    @HasQuantityOf.quantity_pref_unit.setter
    def quantity_pref_unit(self, unit: str) -> None:
        """Sets the quantity pref unit."""
        self._quantity_data['pref_unit'] = self._validate_pref_unit(unit)

    def set_quantity(self, qty: float, unit: str) -> None:
        """Set's the substance's quantity in arbitrary units."""
        # Convert the value into grams;
        g_per_ml = None
        piece_mass_g = None
        if isinstance(self._subject, model.quantity.SupportsExtendedUnits):
            g_per_ml = self._subject.g_per_ml if self._subject.density_is_defined else None
            piece_mass_g = self._subject.piece_mass_g if self._subject.piece_mass_defined else None
        quantity_in_g = model.quantity.convert_qty_unit(
            qty=qty,
            start_unit=unit,
            end_unit='g',
            g_per_ml=g_per_ml,
            piece_mass_g=piece_mass_g
        )

        # Set the values;
        self.quantity_in_g = quantity_in_g
        self.quantity_pref_unit = unit

    def load_data(self, data: 'QuantityData') -> None:
        super().load_data(data)
        self._quantity_data_ = data
