from typing import Any

from model import quantity


def validate_quantity(qty: Any) -> float:
    """Ensures the quantity value is valid, and returns it.
    Raises:
        InvalidQtyError: Indicating the quantity is invalid.
    """
    try:
        qty = float(qty)
    except ValueError:
        raise quantity.exceptions.InvalidQtyError
    if qty < 0:
        raise quantity.exceptions.InvalidQtyError
    else:
        return qty


def validate_qty_unit(unit: Any) -> str:
    """Ensures the unit is a unit which the system recognises, and returns it."""
    for recognised_unit in quantity.get_recognised_qty_units():
        if unit.lower() == recognised_unit.lower():
            return recognised_unit
    raise quantity.exceptions.UnknownUnitError


def validate_mass_unit(unit: Any) -> str:
    """Ensures the unit is a recognised mass unit, and returns it."""
    for recognised_unit in quantity.get_recognised_mass_units():
        if unit.lower() == recognised_unit.lower():
            return recognised_unit
    raise quantity.exceptions.UnknownUnitError


def validate_vol_unit(unit: Any) -> str:
    """Ensures the unit is a recognised volume unit, and returns it."""
    for recognised_unit in quantity.get_recognised_vol_units():
        if unit.lower() == recognised_unit.lower():
            return recognised_unit
    raise quantity.exceptions.UnknownUnitError
