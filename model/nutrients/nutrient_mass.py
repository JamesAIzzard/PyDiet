from typing import TypedDict, Optional

from model import nutrients, quantity


class NutrientMassData(TypedDict):
    """Persistable data format for NutrientTarget data."""
    nutrient_mass_g: Optional[float]
    nutrient_pref_units: str


class NutrientMass:
    def __init__(self, nutrient_name: str, nutrient_mass_g: Optional[float] = None,
                 pref_unit: str = 'g'):
        nutrient_name = nutrients.get_nutrient_primary_name(nutrient_name)
        self._nutrient: 'nutrients.Nutrient' = nutrients.global_nutrients[nutrient_name]
        self._nutrient_mass_g: Optional[float] = nutrient_mass_g
        self._pref_unit: str = pref_unit

    @property
    def nutrient(self) -> 'nutrients.Nutrient':
        """Returns the nutrient associated with the nutrient target."""
        return self._nutrient

    @property
    def nutrient_mass_g(self) -> Optional[float]:
        """Returns the nutrient target mass in grams."""
        return self._nutrient_mass_g

    @property
    def pref_unit(self) -> str:
        """Returns the nutrient mass pref unit."""
        return self._pref_unit

    @property
    def nutrient_mass_in_pref_unit(self) -> Optional[float]:
        """Returns the nutrient mass in the preferred unit."""
        mass_in_pref_unit = quantity.convert_qty_unit(
            qty=self.nutrient_mass_g,
            start_unit='g',
            end_unit=self.pref_unit
        )
        return mass_in_pref_unit

    @property
    def is_defined(self) -> bool:
        """Returns True/False to indicate if the nutrient mass is defined."""
        return self.nutrient_mass_g is not None

    @property
    def is_undefined(self) -> bool:
        """Returns True/False to indicate if the nutrient mass is undefined."""
        return not self.is_defined


class SettableNutrientMass(NutrientMass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @NutrientMass.nutrient_mass_g.setter
    def nutrient_mass_g(self, mass_g: Optional[float]) -> None:
        """Sets the nutrient mass in grams."""
        if mass_g is None:
            self._nutrient_mass_g = None
        else:
            mass_g = quantity.validation.validate_quantity(mass_g)
            self._nutrient_mass_g = mass_g

    def set_nutrient_mass(self, nutrient_mass: Optional[float], nutrient_mass_unit: str = 'g'):
        """Sets the nutrient mass in any unit."""
        if nutrient_mass is None:
            self.nutrient_mass_g = None
            # Also reset pref unit;
            self.pref_unit = 'g'
        else:
            nutrient_mass_g = quantity.convert_qty_unit(
                qty=nutrient_mass,
                start_unit=nutrient_mass_unit,
                end_unit='g'
            )
            self.nutrient_mass_g = nutrient_mass_g
            self.pref_unit = nutrient_mass_unit

    @NutrientMass.pref_unit.setter
    def pref_unit(self, unit: str) -> None:
        """Sets the preff unit for the nutrient mass."""
        unit = quantity.validation.validate_mass_unit(unit)
        self._pref_unit = unit
