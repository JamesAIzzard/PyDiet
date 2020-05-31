from typing import List

_G_CONVERSIONS = {
    "ug": 1e-6,  # 1 microgram = 0.000001 grams
    "mg": 1e-3,  # 1 milligram = 0.001 grams
    "g": 1,  # 1 gram = 1 gram! :)
    "kg": 1e3,  # 1 kilogram = 1000 grams
}

_ML_CONVERSIONS = {
    "ml": 1,
    "cm3": 1,
    "L": 1e3,  # 1L = 1000 ml
    "m3": 1e6,
    "quart": 946.4,
    "tsp": 4.929,
    "tbsp": 14.79
}

class UnknownUnitError(Exception):
    def __init__(self, *args):
        if len(args) and args[0]:
            super().__init__(args[0])

def recognised_mass_units() -> List[str]:
    return list(_G_CONVERSIONS.keys())


def recognised_vol_units() -> List[str]:
    return list(_ML_CONVERSIONS.keys())


def recognised_qty_units() -> List[str]:
    return recognised_mass_units() + \
        recognised_vol_units()


def parse_qty_unit(unit: str) -> str:
    for u in recognised_qty_units():
        if unit.lower() == u.lower():
            return u
    raise UnknownUnitError


def parse_mass_unit(unit: str) -> str:
    for u in recognised_mass_units():
        if unit.lower() == u.lower():
            return u
    raise UnknownUnitError


def parse_vol_unit(unit: str) -> str:
    for u in recognised_vol_units():
        if unit.lower() == u.lower():
            return u
    raise UnknownUnitError


def convert_mass_units(mass: float, start_units: str, end_units: str) -> float:
    # Lowercase all units;
    start_units = start_units.lower()
    end_units = end_units.lower()
    # Convert value to grams first
    mass_in_g = _G_CONVERSIONS[start_units]*mass
    return mass_in_g/_G_CONVERSIONS[end_units]


def convert_volume_units(volume: float, start_units: str, end_units: str) -> float:
    # Parse the units to correct any case differences;
    start_units = parse_qty_unit(start_units)
    end_units = parse_qty_unit(end_units)
    vol_in_ml = _ML_CONVERSIONS[start_units]*volume
    return vol_in_ml/_ML_CONVERSIONS[end_units]


def convert_volume_to_mass(
    volume: float,
    vol_units: str,
    mass_units: str,
    density_g_per_ml: float
) -> float:
    # First convert the volume to ml;
    vol_ml = convert_volume_units(volume, vol_units, 'ml')
    # Calculate mass in g;
    mass_g = density_g_per_ml*vol_ml
    # Convert the mass to putput units;
    mass_output = convert_mass_units(mass_g, 'g', mass_units)
    # Return result;
    return mass_output



