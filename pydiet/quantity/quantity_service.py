from typing import List, Any, Optional

from pydiet import quantity


def get_recognised_mass_units() -> List[str]:
    return list(quantity.configs.G_CONVERSIONS.keys())


def get_recognised_vol_units() -> List[str]:
    return list(quantity.configs.ML_CONVERSIONS.keys())


def get_recognised_qty_units() -> List[str]:
    return get_recognised_mass_units() + \
        get_recognised_vol_units()


def unit_is_mass(unit: str) -> bool:
    return unit in get_recognised_mass_units()


def unit_is_volume(unit: str) -> bool:
    return unit in get_recognised_vol_units()


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


def convert_qty_unit(qty: float,
                     start_unit=str,
                     end_unit=str,
                     density_g_per_ml: Optional[float] = None) -> float:

    # Validate all units to correct any case issues;
    start_unit = validate_qty_unit(start_unit)
    end_unit = validate_qty_unit(end_unit)

    # If we don't need density;
    if unit_is_mass(start_unit) and unit_is_mass(end_unit) or \
            unit_is_volume(start_unit) and unit_is_volume(end_unit):
        # Nuke it;
        density_g_per_ml = 1

    # u_out = k(rho*unit_in) => k = (rho*u_in)/u_out
    g_convs = quantity.configs.G_CONVERSIONS
    ml_convs = quantity.configs.ML_CONVERSIONS
    if unit_is_mass(start_unit):
        u_in = g_convs[start_unit]
    else:  # Start unit is vol.
        u_in = ml_convs[start_unit]
    if unit_is_mass(end_unit):
        u_out = g_convs[end_unit]
        density_g_per_ml = 1/density_g_per_ml # Flip density when going vol->mass
    else:  # End unit is vol.
        u_out = ml_convs[end_unit]
    k = (density_g_per_ml*u_in)/u_out

    return qty*k


def convert_density_unit(qty: float,
                         start_mass_unit: str,
                         start_vol_unit: str,
                         end_mass_unit: str,
                         end_vol_unit: str) -> float:

    # Validate all units to correct any case issues;
    start_mass_unit = validate_mass_unit(start_mass_unit)
    start_vol_unit = validate_vol_unit(start_vol_unit)
    end_mass_unit = validate_mass_unit(end_mass_unit)
    end_vol_unit = validate_vol_unit(end_vol_unit)

    # m_in/v_in = k(m_out/v_out) => k = (m_in*v_out)/(v_in*m_out)
    g_convs = quantity.configs.G_CONVERSIONS
    ml_convs = quantity.configs.ML_CONVERSIONS
    m_in = g_convs[start_mass_unit]
    m_out = g_convs[end_mass_unit]
    v_in = ml_convs[start_vol_unit]
    v_out = ml_convs[end_vol_unit]
    k = (m_in*v_out)/(m_out*v_in)

    return qty*k
