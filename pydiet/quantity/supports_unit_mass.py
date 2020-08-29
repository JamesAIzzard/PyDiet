import abc

from typing import Optional, Protocol, TypedDict


class UnitMassData(TypedDict):
    unit_mass_g: Optional[float]
    unit_mass_pref_units: Optional[str]


unit_mass_template = {
    "unit_mass_g": None,
    "unit_mass_pref_units": None
}


class SupportsUnitMass(Protocol):
    
    @abc.abstractproperty
    def readonly_unit_mass_data(self) -> 'UnitMassData':
        raise NotImplementedError
