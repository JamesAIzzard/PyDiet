from typing import Tuple, TYPE_CHECKING

from pyconsoleapp import ResponseValidationError, validators

from pydiet import quantity

if TYPE_CHECKING:
    from pydiet.quantity import HasBulk


def validate_mass_unit(unit: str) -> str:
    """Parses and returns any valid mass unit."""
    try:
        unit = quantity.validation.validate_mass_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError('The unit is not a recognised mass.')
    return unit


def validate_vol_unit(unit: str) -> str:
    """Parses and returns any valid vol unit."""
    try:
        unit = quantity.validation.validate_vol_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError('The unit is not a recognised volume.')
    return unit


def validate_unit(unit: str) -> str:
    """Parses and returns any valid unit."""
    try:
        unit = quantity.validation.validate_qty_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError(
            'The unit is not recognised.')
    return unit


def validate_configured_unit(subject: 'HasBulk', unit: str) -> str:
    """Parses and returns any unit which is valid and has been
    configured on the _subject."""
    unit = validate_unit(unit)
    if quantity.core.units_are_volumes(unit) and not subject.density_is_defined:
        raise ResponseValidationError(
            'Density must be set before volumetric measurements can be used.')
    elif quantity.core.units_are_pieces(unit) and not subject.piece_mass_defined:
        raise ResponseValidationError(
            'Piece mass must be set before pieces can be used.')
    return unit


def validate_volume_qty_and_unit(qty_and_unit: str) -> Tuple[float, str]:
    """Parses a string containing qty and unit, and returns a tuple containing
    the qty and unit seperately. Also checks the qty is a valid qty and the unit is a known unit."""
    qty, unit = validators.validate_number_and_str(qty_and_unit)
    qty = validators.validate_positive_nonzero_number(qty)
    unit = validate_vol_unit(unit)
    return qty, unit


def validate_mass_qty_and_unit(qty_and_unit: str) -> Tuple[float, str]:
    """Parses a string containing a qty and unit and returns a tuple containing the qty and mass unit
    seperately. Checks the quantity is a valid quantity, and the unit is a valid mass unit."""
    qty, unit = validators.validate_number_and_str(qty_and_unit)
    qty = validators.validate_positive_nonzero_number(qty)
    unit = validate_mass_unit(unit)
    return qty, unit
