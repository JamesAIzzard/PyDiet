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
