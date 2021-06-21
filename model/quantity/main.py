"""Utility functions for the quantity module."""
from typing import Optional

import model.quantity


def get_ratio_from_qty_ratio_data(qr_data: 'model.quantity.QuantityRatioData') -> float:
    """Return the ratio from the quantity ratio data."""
    return qr_data['subject_qty_data']['quantity_in_g'] / qr_data['host_qty_data']['quantity_in_g']


def quantity_ratio_data_is_defined(qr_data: 'model.quantity.QuantityRatioData') -> bool:
    """Returns True/False to indicate if quantity ratio data is defined."""
    return qr_data['subject_qty_data']['quantity_in_g'] is not None and qr_data['host_qty_data'][
        'quantity_in_g'] is not None


def undefine_qty_ratio(quantity_ratio: 'model.quantity.IsQuantityRatioBase') -> None:
    """Undefines the quantity ratio provided."""
    for qi in [quantity_ratio.ratio_host_qty, quantity_ratio.ratio_subject_qty]:
        assert (isinstance(qi, model.quantity.IsSettableQuantityOf))
        qi.unset_quantity()


def zero_qty_ratio(quantity_ratio: 'model.quantity.IsQuantityRatioBase') -> None:
    """Zeroes the quantity ratio provided."""
    for qi in [quantity_ratio.ratio_host_qty, quantity_ratio.ratio_subject_qty]:
        assert (isinstance(qi, model.quantity.IsSettableQuantityOf))
        qi.set_quantity(quantity_value=0)


def units_are_masses(*units: str) -> bool:
    """Returns True/False to indicate if EVERY parameter is a mass unit."""
    for unit in units:
        if unit.lower() not in model.quantity.MASS_UNITS:
            return False
    return True


def units_are_volumes(*units: str) -> bool:
    """Returns True/False to indicate if EVERY parameter is a volumetric unit."""
    for unit in units:
        if unit.lower() not in model.quantity.VOL_UNITS:
            return False
    return True


def units_are_pieces(*units: str) -> bool:
    """Returns True or false to indicate if EVERY unit is the piece unit."""
    for unit in units:
        if unit.lower() not in model.quantity.PC_UNITS:
            return False
    return True


def unit_is_extended(unit: str) -> bool:
    """Returns True/False to indicate if unit is extended."""
    unit = model.quantity.validation.validate_qty_unit(unit)
    if units_are_pieces(unit) or units_are_volumes(unit):
        return True
    else:
        return False


def _convert_like2like(qty: float, start_unit: str, end_unit: str) -> float:
    """Handles mass<->mass and vol<->vol"""
    # Validate the units;
    start_unit = start_unit.lower()
    end_unit = end_unit.lower()
    for u in [start_unit, end_unit]:
        model.quantity.validation.validate_qty_unit(u)

    # Make sure both units are the same kind;
    if not units_are_masses(start_unit, end_unit) and not units_are_volumes(start_unit, end_unit):
        raise model.quantity.exceptions.IncorrectUnitTypeError()

    # Figure out the conversion factor;
    if units_are_masses(start_unit, end_unit):
        u_i = model.quantity.configs.G_CONVERSIONS[start_unit]
        u_o = model.quantity.configs.G_CONVERSIONS[end_unit]
    elif units_are_volumes(start_unit, end_unit):
        u_i = model.quantity.configs.ML_CONVERSIONS[start_unit]
        u_o = model.quantity.configs.ML_CONVERSIONS[end_unit]
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
    """Converts any quantity unit to any other quantity unit."""

    # Correct unit case issues and raise an exception if the unit isn't recognised;
    start_unit = model.quantity.validation.validate_qty_unit(start_unit)
    end_unit = model.quantity.validation.validate_qty_unit(end_unit)

    # like2like;
    if units_are_masses(start_unit, end_unit) or \
            units_are_volumes(start_unit, end_unit) or \
            units_are_pieces(start_unit, end_unit):
        return _convert_like2like(qty, start_unit, end_unit)

    # mass<->vol;
    elif (units_are_masses(start_unit) and units_are_volumes(end_unit)) or \
            (units_are_volumes(start_unit) and units_are_masses(end_unit)):
        if g_per_ml is None:
            raise model.quantity.exceptions.UndefinedDensityError()
        return _convert_mass_and_vol(qty, start_unit, end_unit, g_per_ml)

    # pc<->mass;
    elif (units_are_pieces(start_unit) and units_are_masses(end_unit)) or \
            (units_are_masses(start_unit) and units_are_pieces(end_unit)):
        if piece_mass_g is None:
            raise model.quantity.exceptions.UndefinedPcMassError()
        return _convert_pc_and_mass(qty, start_unit, end_unit, piece_mass_g)

    # pc->vol;
    elif (units_are_pieces(start_unit) and units_are_volumes(end_unit)) or \
            (units_are_volumes(start_unit) and units_are_pieces(end_unit)):
        if piece_mass_g is None:
            raise model.quantity.exceptions.UndefinedPcMassError()
        if g_per_ml is None:
            raise model.quantity.exceptions.UndefinedDensityError()
        return _convert_pc_and_vol(qty, start_unit, end_unit, piece_mass_g, g_per_ml)

    else:
        raise LookupError('Unable to find a converter for this combination of units.')


def convert_density_unit(qty: float,
                         start_mass_unit: str,
                         start_vol_unit: str,
                         end_mass_unit: str,
                         end_vol_unit: str,
                         piece_mass_g: Optional[float] = None) -> float:
    """Converts any density unit to any other density unit."""

    # Catch any invalid quantities;
    qty = model.quantity.validation.validate_quantity(qty)
    if piece_mass_g is not None:
        piece_mass_g = model.quantity.validation.validate_quantity(piece_mass_g)

    # Handle pc being used as the start mass unit;
    if units_are_pieces(start_mass_unit):
        start_mass_unit = 'g'
        qty = piece_mass_g * qty

    # Handle pc being used as the end mass unit;
    if units_are_pieces(end_mass_unit):
        end_mass_unit = 'g'
        qty = qty / piece_mass_g

    # Validate all units to correct any case issues;
    start_mass_unit = model.quantity.validation.validate_mass_unit(start_mass_unit)
    start_vol_unit = model.quantity.validation.validate_vol_unit(start_vol_unit)
    end_mass_unit = model.quantity.validation.validate_mass_unit(end_mass_unit)
    end_vol_unit = model.quantity.validation.validate_vol_unit(end_vol_unit)

    # m_in/v_in = k(m_out/v_out) => k = (m_in*v_out)/(v_in*m_out)
    # Shortcut the conversion tables;
    g_convs = model.quantity.configs.G_CONVERSIONS
    ml_convs = model.quantity.configs.ML_CONVERSIONS
    # Set the conversion factors;
    m_in = g_convs[start_mass_unit]
    m_out = g_convs[end_mass_unit]
    v_in = ml_convs[start_vol_unit]
    v_out = ml_convs[end_vol_unit]
    # Calc ratio;
    k = (m_in * v_out) / (m_out * v_in)

    return qty * k
