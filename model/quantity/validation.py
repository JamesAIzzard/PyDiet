"""Defines the validation functionality associated with the quantity module."""
from typing import Any

import model


def validate_quantity(qty: float) -> float:
    """Ensures the quantity value is valid, and returns it.
    Raises:
        InvalidQtyError: Indicating the quantity is invalid.
    """
    try:
        qty = float(qty)
    except ValueError:
        raise model.quantity.exceptions.InvalidQtyError(quantity=qty)
    if qty < 0:
        raise model.quantity.exceptions.InvalidQtyError(quantity=qty)
    else:
        return qty


def validate_nonzero_quantity(qty: Any) -> float:
    """Ensures the quantity value is valid and nonzero, and returns it.
    Raises:
        InvalidQtyError: Indicating the quantity is invalid.
    """
    qty = validate_quantity(qty)
    if qty == 0:
        raise model.quantity.exceptions.ZeroQtyError()
    else:
        return qty


def validate_qty_unit(unit: str) -> str:
    """Ensures the unit is a unit which the system recognises, and returns it."""
    # All units are in lowercase;
    unit = unit.lower()
    # Raise an exception if the unit isn't in the system;
    if unit not in model.quantity.QTY_UNITS:
        raise model.quantity.exceptions.UnknownUnitError(unit=unit)
    # All must be OK, return it;
    return unit


def validate_mass_unit(unit: str) -> str:
    """Ensures the unit is a recognised mass unit, and returns it."""
    # All units are in lowercase;
    unit = unit.lower()
    # Raise an exception if the unit isn't in the system;
    if unit not in model.quantity.QTY_UNITS:
        raise model.quantity.exceptions.UnknownUnitError(unit=unit)
    # Raise an exception if the unit is in the system, but isn't a mass;
    if unit not in model.quantity.MASS_UNITS:
        raise model.quantity.exceptions.IncorrectUnitTypeError(unit=unit)
    # All must be OK, return it;
    return unit


def validate_vol_unit(unit: str) -> str:
    """Ensures the unit is a recognised volume unit, and returns it."""
    # All units are in lowercase;
    unit = unit.lower()
    # Raise an exception if the unit isn't in the system;
    if unit not in model.quantity.QTY_UNITS:
        raise model.quantity.exceptions.UnknownUnitError(unit=unit)
    # Raise an exception if the unit is in the system, but isn't a volume;
    if unit not in model.quantity.VOL_UNITS:
        raise model.quantity.exceptions.IncorrectUnitTypeError(unit=unit)
    # All must be OK, return it;
    return unit


def validate_pc_unit(unit: str) -> str:
    """Ensures the unit is a recognised pc mass unit, and returns it."""
    # All units are in lowercase;
    unit = unit.lower()
    # Raise an exception if the unit isn't in the system;
    if unit not in model.quantity.QTY_UNITS:
        raise model.quantity.exceptions.UnknownUnitError(unit=unit)
    # Raise an exception if the unit is in the system, but isn't a volume;
    if unit not in model.quantity.PC_UNITS:
        raise model.quantity.exceptions.IncorrectUnitTypeError(unit=unit)
    # All must be OK, return it;
    return unit


def validate_pref_unit(unit: str, subject: Any) -> str:
    """Validates the provided unit in the context of the subject provided.
    Raises exceptions for any of the normal reasons, but also if the unit
    is not configured on the subject.
    """
    # First, check the unit is known by the system;
    unit = model.quantity.validation.validate_qty_unit(unit)

    # If the subject doesn't support extended units, and the unit is a mass or volume;
    if model.quantity.unit_is_extended(unit) \
            and not isinstance(subject, model.quantity.SupportsExtendedUnits):
        raise model.quantity.exceptions.UnsupportedExtendedUnitsError(subject=subject)

    # OK, so the subject does support extended units;
    # If the unit is a volume, and the subject doesn't have density defined;
    if model.quantity.units_are_volumes(unit) and not subject.density_is_defined:
        raise model.quantity.exceptions.UndefinedDensityError(subject=subject)
    elif model.quantity.units_are_pieces(unit) and not subject.piece_mass_is_defined:
        raise model.quantity.exceptions.UndefinedPcMassError(subject=subject)

    # OK, return the unit;
    return unit
