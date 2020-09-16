from typing import Any, TYPE_CHECKING

from pyconsoleapp import ResponseValidationError

from pydiet import quantity

if TYPE_CHECKING:
    from pydiet.quantity.supports_bulk import SupportsBulk


def validate_unit(subject: 'SupportsBulk', unit:Any) -> str:
    try:
        unit = quantity.quantity_service.validate_qty_unit(unit)
    except quantity.exceptions.UnknownUnitError:
        raise ResponseValidationError(
            'The unit is not recognised.')
    if quantity.quantity_service.units_are_volumes(unit) and not subject.density_is_defined:
        raise ResponseValidationError(
            'Density must be set before volumetric measurements can be used.')
    elif quantity.quantity_service.units_are_pieces(unit) and not subject.piece_mass_defined:
        raise ResponseValidationError(
            'Piece mass must be set before pieces can be used.')
    return unit