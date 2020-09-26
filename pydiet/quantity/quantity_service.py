from typing import List, Any, Optional

from pydiet import quantity


def get_recognised_mass_units() -> List[str]:
    return list(quantity.configs.G_CONVERSIONS.keys())


def get_recognised_vol_units() -> List[str]:
    return list(quantity.configs.ML_CONVERSIONS.keys())


def get_recognised_qty_units() -> List[str]:
    return get_recognised_mass_units() + \
           get_recognised_vol_units() + ['pc']


def units_are_masses(*units: str) -> bool:
    for unit in units:
        if unit not in get_recognised_mass_units():
            return False
    return True


def units_are_volumes(*units: str) -> bool:
    for unit in units:
        if unit not in get_recognised_vol_units():
            return False
    return True


def units_are_pieces(*units: str) -> bool:
    for unit in units:
        if not unit.lower() == 'pc':
            return False
    return True


def _convert_like2like(qty: float, start_unit: str, end_unit: str) -> float:
    """Handles mass<->mass and vol<->vol"""
    if units_are_masses(start_unit, end_unit):
        u_i = quantity.configs.G_CONVERSIONS[start_unit]
        u_o = quantity.configs.G_CONVERSIONS[end_unit]
    elif units_are_volumes(start_unit, end_unit):
        u_i = quantity.configs.ML_CONVERSIONS[start_unit]
        u_o = quantity.configs.ML_CONVERSIONS[end_unit]
    else:  # Units are pieces.
        u_i = 1
        u_o = 1
    k = u_i / u_o
    return qty * k


def _convert_mass_and_vol(qty: float, start_unit: str, end_unit: str, g_per_ml: float) -> float:
    """Handles mass<->vol and vol<->mass"""
    if units_are_masses(start_unit):  # Start unit is mass.
        qty_g = _convert_like2like(qty, start_unit, 'g')
        qty_ml = qty_g / g_per_ml
        return _convert_like2like(qty_ml, 'ml', end_unit)  # Return vol.
    else:  # Start unit is vol.
        qty_ml = _convert_like2like(qty, start_unit, 'ml')
        qty_g = qty_ml * g_per_ml
        return _convert_like2like(qty_g, 'g', end_unit)


def _convert_pc_and_mass(qty: float, start_unit: str, end_unit: str, piece_mass_g: float) -> float:
    """Handles pc<->mass and mass<->pc"""
    if units_are_pieces(start_unit):  # Start unit is pc.
        qty_g = qty * piece_mass_g
        return _convert_like2like(qty_g, 'g', end_unit)  # Return mass.
    else:  # Start unit is mass.
        qty_g = _convert_like2like(qty, start_unit, 'g')
        return qty_g / piece_mass_g  # Return pieces.


def _convert_pc_and_vol(qty: float, start_unit: str, end_unit: str, piece_mass_g: float, g_per_ml: float) -> float:
    """Handles pc<->vol and vol<->pc"""
    if units_are_pieces(start_unit):  # Start unit is pc.
        qty_g = _convert_pc_and_mass(qty, 'pc', 'g', piece_mass_g)
        return _convert_mass_and_vol(qty_g, 'g', end_unit, g_per_ml)  # Return vol.
    else:  # Start unit is vol.
        qty_ml = _convert_like2like(qty, start_unit, 'ml')
        qty_g = _convert_mass_and_vol(qty_ml, 'ml', 'g', g_per_ml)
        return _convert_pc_and_mass(qty_g, 'g', 'pc', piece_mass_g)  # Return pieces.


def convert_qty_unit(qty: float,
                     start_unit: str,
                     end_unit: str,
                     g_per_ml: Optional[float] = None,
                     piece_mass_g: Optional[float] = None) -> float:
    # Validate all units to correct any case issues;
    start_unit = validate_qty_unit(start_unit)
    end_unit = validate_qty_unit(end_unit)

    # like2like
    if units_are_masses(start_unit, end_unit) or \
            units_are_volumes(start_unit, end_unit) or \
            units_are_pieces(start_unit, end_unit):
        return _convert_like2like(qty, start_unit, end_unit)

    # mass<->vol
    elif (units_are_masses(start_unit) and units_are_volumes(end_unit)) or \
            (units_are_volumes(start_unit) and units_are_masses(end_unit)):
        if g_per_ml is None:
            raise ValueError('g_per_ml cannot be None for mass<->vol conversions.')
        return _convert_mass_and_vol(qty, start_unit, end_unit, g_per_ml)

    # pc<->mass
    elif (units_are_pieces(start_unit) and units_are_masses(end_unit)) or \
            (units_are_masses(start_unit) and units_are_pieces(end_unit)):
        if piece_mass_g is None:
            raise ValueError('piece_mass_g cannot be None for pc<->mass conversions.')
        return _convert_pc_and_mass(qty, start_unit, end_unit, piece_mass_g)

    # pc->vol
    elif (units_are_pieces(start_unit) and units_are_volumes(end_unit)) or \
            (units_are_volumes(start_unit) and units_are_pieces(end_unit)):
        if piece_mass_g is None:
            raise ValueError('piece_mass_g cannot be None for pc<->vol conversions.')
        if g_per_ml is None:
            raise ValueError('g_per_ml cannot be None pc<->vol conversions.')
        return _convert_pc_and_vol(qty, start_unit, end_unit, piece_mass_g, g_per_ml)

    else:
        raise LookupError('Unable to find a converter for this combination of units.')


def convert_density_unit(qty: float,
                         start_mass_unit: str,
                         start_vol_unit: str,
                         end_mass_unit: str,
                         end_vol_unit: str,
                         piece_mass_g: Optional[float] = None) -> float:
    # Handle pc being used as the start mass unit;
    if units_are_pieces(start_mass_unit):
        start_mass_unit = 'g'
        qty = piece_mass_g * qty

    # Handle pc being used as the end mass unit;
    if units_are_pieces(end_mass_unit):
        end_mass_unit = 'g'
        qty = qty / piece_mass_g

    # Validate all units to correct any case issues;
    start_mass_unit = validate_mass_unit(start_mass_unit)
    start_vol_unit = validate_vol_unit(start_vol_unit)
    end_mass_unit = validate_mass_unit(end_mass_unit)
    end_vol_unit = validate_vol_unit(end_vol_unit)

    # m_in/v_in = k(m_out/v_out) => k = (m_in*v_out)/(v_in*m_out)
    # Shortcut the conversion tables;
    g_convs = quantity.configs.G_CONVERSIONS
    ml_convs = quantity.configs.ML_CONVERSIONS
    # Set the conversion factors;
    m_in = g_convs[start_mass_unit]
    m_out = g_convs[end_mass_unit]
    v_in = ml_convs[start_vol_unit]
    v_out = ml_convs[end_vol_unit]
    # Calc ratio;
    k = (m_in * v_out) / (m_out * v_in)

    return qty * k


def validate_quantity(value: Any) -> float:
    value = float(value)
    if value <= 0:
        raise quantity.exceptions.InvalidQtyError
    else:
        return value


def validate_qty_unit(unit: str) -> str:
    for u in get_recognised_qty_units():
        if unit.lower() == u.lower():
            return u
    raise quantity.exceptions.UnknownUnitError


def validate_mass_unit(unit: str) -> str:
    for u in get_recognised_mass_units():
        if unit.lower() == u.lower():
            return u
    raise quantity.exceptions.UnknownUnitError


def validate_vol_unit(unit: str) -> str:
    for u in get_recognised_vol_units():
        if unit.lower() == u.lower():
            return u
    raise quantity.exceptions.UnknownUnitError
