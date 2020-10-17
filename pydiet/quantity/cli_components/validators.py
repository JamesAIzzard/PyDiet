from typing import TypedDict, TYPE_CHECKING

from pyconsoleapp import ResponseValidationError, builtin_validators
from pydiet import quantity

if TYPE_CHECKING:
    from pydiet.quantity.supports_bulk import SupportsBulk


class QtyAndUnit(TypedDict):
    qty: float
    unit: str


def validate_mass_unit(unit: str) -> str:
    """Parses and returns any valid mass unit."""
    try:
        unit = quantity.services.validate_mass_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError('The unit is not a recognised mass.')
    return unit


def validate_vol_unit(unit: str) -> str:
    """Parses and returns any valid vol unit."""
    try:
        unit = quantity.services.validate_vol_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError('The unit is not a recognised volume.')
    return unit


def validate_unit(unit: str) -> str:
    """Parses and returns any valid unit."""
    try:
        unit = quantity.services.validate_qty_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError(
            'The unit is not recognised.')
    return unit


def validate_configured_unit(subject: 'SupportsBulk', unit: str) -> str:
    """Parses and returns any unit which is valid and has been
    configured on the _subject."""
    unit = validate_unit(unit)
    if quantity.services.units_are_volumes(unit) and not subject.density_is_defined:
        raise ResponseValidationError(
            'Density must be set before volumetric measurements can be used.')
    elif quantity.services.units_are_pieces(unit) and not subject.piece_mass_defined:
        raise ResponseValidationError(
            'Piece mass must be set before pieces can be used.')
    return unit


def validate_volume_qty_and_unit(value: str) -> QtyAndUnit:
    qty, unit = builtin_validators.validate_number_and_str(value)
    qty = builtin_validators.validate_positive_nonzero_number(qty)
    unit = validate_vol_unit(unit)
    return QtyAndUnit(qty=qty, unit=unit)


def validate_mass_qty_and_unit(value: str) -> QtyAndUnit:
    qty, unit = builtin_validators.validate_number_and_str(value)
    qty = builtin_validators.validate_positive_nonzero_number(qty)
    unit = validate_mass_unit(unit)
    return QtyAndUnit(qty=qty, unit=unit)
