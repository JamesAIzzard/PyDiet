import abc
from typing import Dict, TypedDict, Optional

from model import nutrients, quantity


class GoalsData(TypedDict):
    flags: Dict[str, Optional[bool]]
    max_cost_gbp_target: Optional[float]
    calorie_target: Optional[float]
    nutrient_mass_goals: Dict[str, 'nutrients.NutrientMassData']


class HasSettableGoals(abc.ABC):
    """Defines the functionality of classes on which optimsiation goals can be set.
    Provides implementations where possible.
    Note:
        These methods must not expose the internal SettableNutrientMass objects, because we
        need to control when they can be set, based on the broader state of DayGoals and
        MealGoals objects. If we hand out mutable objects representing nutrient mass goals to
        the rest of the applications, controlling when the can be set, and when setting raises
        an exception, is a much more involved process.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Init dictionary for nutrient mass targets;
        self._nutrient_mass_targets: Dict[str, 'nutrients.SettableNutrientMass'] = {}
        for nutrient_name in nutrients.all_primary_nutrient_names:
            self._nutrient_mass_targets[nutrient_name] = nutrients.SettableNutrientMass(nutrient_name=nutrient_name)

    def get_nutrient_mass_goal(self, nutrient_name: str, unit: Optional[str] = None) -> Optional[float]:
        """Returns the named nutrient mass target in pref units, Unless other unit is specified."""
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)

        # Handle unset goal;
        if self._nutrient_mass_targets[nutrient_name].nutrient_mass_g is None:
            return None

        # If unit is unspecified, return in pref unit;
        if unit is None:
            return self._nutrient_mass_targets[nutrient_name].nutrient_mass_in_pref_unit

        # Otherwise, convert to requested unit;
        if unit is not None:
            mass_g = self._nutrient_mass_targets[nutrient_name].nutrient_mass_g
            return quantity.convert_qty_unit(
                qty=mass_g,
                start_unit='g',
                end_unit=unit
            )

    def set_nutrient_mass_goal(self, nutrient_name: str, nutrient_mass: Optional[float] = None,
                               nutrient_mass_unit: str = 'g') -> None:
        """Sets the named nutrient mass goal the the mass/unit specified."""
        # Validate the nutrient name;
        nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)

        # If we are unsetting nutrient mass;
        if nutrient_mass is None:
            self._nutrient_mass_targets[nutrient_name].nutrient_mass_g = None
            self._nutrient_mass_targets[nutrient_name].pref_unit = 'g'

        # If we are setting to a value;
        else:
            self._nutrient_mass_targets[nutrient_name].set_nutrient_mass(
                nutrient_mass=nutrient_mass,
                nutrient_mass_unit=nutrient_mass_unit
            )

    def unset_nutrient_mass_goal(self, nutrient_name: str) -> None:
        """Unsets the named nutrient mass goal."""
        self.set_nutrient_mass_goal(nutrient_name, None)
