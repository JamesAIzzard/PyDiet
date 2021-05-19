import abc
from typing import List, Dict, TypedDict, Optional, Any

import goals
import model
import model.nutrients.main
import persistence


class GoalsData(TypedDict):
    """Persistable data format for objects with goals."""
    flags: Dict[str, Optional[bool]]
    max_cost_gbp_target: Optional[float]
    calorie_target: Optional[float]
    nutrient_mass_goals: Dict[str, 'model.nutrients.NutrientMassData']


class HasSettableGoals(persistence.HasPersistableData, abc.ABC):
    """Defines the functionality of classes on which optimsiation goals can be set.
    Provides implementations where possible.
    Note:
        These methods must not expose the internal SettableNutrientMass objects, because we
        need to control when they can be set, based on the broader state of DayGoals and
        MealGoals objects. If we hand out mutable objects representing nutrient mass goals to
        the rest of the applications, controlling when the can be set, and when setting raises
        an exception, is a much more involved process.
    """

    def __init__(self, goals_data: Optional['GoalsData'] = None, **kwargs):
        super().__init__(**kwargs)

        # Don't just store the data object here, because we need to instantiate SettableNutrientMass
        # instances to represent the data inside it. It would be messy and confusing to store the
        # the flags and other stuff in the TypedDict, and then just the nutrient mass targets here.
        self._flags: Dict[str, Optional[bool]] = {}
        self._max_cost_gbp_target: Optional[float] = None
        self._calorie_target: Optional[float] = None
        self._nutrient_mass_goals: Dict[str, 'model.nutrients.SettableNutrientMass'] = {}

        # Load the data into the instance if provided;
        if goals_data is not None:
            self.load_data(goals_data)

    @property
    def max_cost_gbp_target(self) -> float:
        """Returns the target max cost gbp for the instance."""
        # If the target isn't defined, raise an exception;
        if self._max_cost_gbp_target is None:
            raise goals.exceptions.UndefinedMaxCostTargetError(subject=self)
        else:
            return self._max_cost_gbp_target

    @max_cost_gbp_target.setter
    def max_cost_gbp_target(self, max_cost_gbp_target: Optional[float]) -> None:
        """Sets the target max cost gbp for the MealGoals instance."""
        if max_cost_gbp_target is None:
            self._max_cost_gbp_target = None
        else:
            self._max_cost_gbp_target = model.cost.validation.validate_cost(max_cost_gbp_target)

    @property
    def calorie_target(self) -> float:
        """Returns the calorie target for the MealGoals instance."""
        if self._calorie_target is None:
            raise goals.exceptions.UndefinedCalorieTargetError(subject=self)
        return self._calorie_target

    @calorie_target.setter
    def calorie_target(self, calorie_target: Optional[float]) -> None:
        """Sets the calorie target for the MealGoals instance."""
        if calorie_target is None:
            self._calorie_target = None
        else:
            self._calorie_target = model.quantity.validation.validate_quantity(calorie_target)

    @property
    def targeted_nutrient_names(self) -> List[str]:
        """Returns a list of all nutrient names with goals associated with them."""
        return list(self._nutrient_mass_goals.keys())

    def nutrient_mass_goal_is_defined(self, nutrient_name: str) -> bool:
        """Returns True/False to indicate if the nutrient mass goal is defined."""
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)
        return nutrient_name in self.targeted_nutrient_names

    def get_nutrient_mass_goal(self, nutrient_name: str) -> 'model.nutrients.NutrientMass':
        """Returns a non-writable nutrient mass instance. See note in class docstring for
        reasoning behind returning the non-writeable version."""

        # Convert the SettableNutrientMass instance into a readonly version;
        settable_nm = self._get_settable_nutrient_mass_goal(nutrient_name)
        return model.nutrients.NutrientMass(nutrient_mass_data=settable_nm.persistable_data)

    def _get_settable_nutrient_mass_goal(self, nutrient_name: str) -> 'model.nutrients.SettableNutrientMass':
        """Returns a the specified settable nutrient mass goal.
        Notes:
            Internal use only! See not in class docstring. DO NOT GIVE THESE INSTANCES OUT!
        """
        # Validate nutrient name;
        nutrient_name = model.nutrients.main.validate_nutrient_name(nutrient_name)

        # If we don't have a goal for this nutrient;
        if nutrient_name not in self.targeted_nutrient_names:
            raise goals.exceptions.UndefinedNutrientMassGoalError(
                subject=self,
                nutrient_name=nutrient_name
            )

        # Go ahead and return the instance;
        return self._nutrient_mass_goals[nutrient_name]

    def set_nutrient_mass_goal(self, nutrient_name: str, nutrient_mass: Optional[float] = None,
                               nutrient_mass_unit: str = 'g') -> None:
        """Sets the named nutrient mass goal the the mass/unit specified. Invokes validation and resets the
        original value if there was a problem.
        """

        # Validate the nutrient name;
        nutrient_name = model.nutrients.get_nutrient_primary_name(nutrient_name)

        # If we are unsetting nutrient mass;
        if nutrient_mass is None:
            del self._nutrient_mass_goals[nutrient_name]
            return

        # OK, because we are setting to a real value, we need to take a backup in case we cause a conflict somewhere;
        # Note: Although our backup is a mutable object, it won't update when we update the goal
        # value later on, because it is an independent settable only version of the writable version stored by
        # the MealGoals instance.
        backup_mass_goal = self.get_nutrient_mass_goal(nutrient_name)

        try:
            # Go ahead and set;
            self._nutrient_mass_goals[nutrient_name].set_nutrient_mass(
                nutrient_mass=nutrient_mass,
                nutrient_mass_unit=nutrient_mass_unit
            )
            # Now run validation to make sure we haven't caused mutual inconsistencies;
            self.validate_nutrient_mass_goal(nutrient_name)
        except(
                ValueError,  # Mass value is not a valid qty.
                model.quantity.exceptions.UnknownUnitError,  # The unit isn't recognised at all.
                model.quantity.exceptions.IncorrectUnitTypeError,  # The unit isn't a mass.
                # Nutrient mass causes a conflict with other defined nutrients in the family.
                model.nutrients.exceptions.NutrientFamilyConflictError,
        ) as err:
            # OK, something went wrong, so replace the backup value and re-raise the error.
            self._get_settable_nutrient_mass_goal(nutrient_name).load_data(backup_mass_goal.persistable_data)
            raise err

    def validate_nutrient_mass_goal(self, nutrient_name: str) -> None:
        """Checks the nutrient mass goal for conflicts with family nutrient mass goals *on this instance*."""
        _ = model.nutrients.validate_nutrient_family_masses(
            nutrient_name=nutrient_name,
            nutrient_mass_g=self.get_nutrient_mass_goal(nutrient_name).nutrient_mass_g,
            get_nutrient_mass_g=lambda: self.get_nutrient_mass_goal(nutrient_name).nutrient_mass_g
        )

    def undefine_nutrient_mass_goal(self, nutrient_name: str) -> None:
        """Unsets the named nutrient mass goal."""
        self.set_nutrient_mass_goal(nutrient_name, None)

    @property
    def persistable_data(self) -> Dict[str, Any]:
        """Returns GoalsData for this instance.
        Notes:
            It is important to note that this is only the data associated directly with this instance.
            In the context of a DayGoals class, this data wouldn't contain the nutrient mass goals
            associated with any MealGoals attached to the DayGoals instance - only the goals associated
            with the DayGoals instance at the DayGoals level.
        """
        # Get any data from related classes;
        data = super().persistable_data
        # Fill in the easy ones first;
        data['flags'] = self._flags
        data['max_cost_gbp_target'] = self._max_cost_gbp_target
        data['calorie_target'] = self._max_cost_gbp_target
        # Now compile the nutrient mass goals;
        nutrient_mass_goals = {}
        for nutrient_name, nutrient_mass in self._nutrient_mass_goals.items():
            nutrient_mass_goals[nutrient_name] = nutrient_mass.persistable_data
        data['nutrient_mass_goals'] = nutrient_mass_goals
        # Return the lot;
        return data

    def load_data(self, data: 'GoalsData'):
        """Loads a GoalsData dict into the instance."""
        # Pass the data dict on to sibling classes;
        super().load_data(data)
        # First, load the easy stuff;
        self._flags = data['flags']
        self._max_cost_gbp_target = data['max_cost_gbp_target']
        self._calorie_target = data['calorie_target']

        # Load in the nutrient mass goals;
        for nutrient_name, nutrient_mass_data in data['nutrient_mass_goals'].items():
            self._nutrient_mass_goals[nutrient_name] = model.nutrients.SettableNutrientMass(
                nutrient_mass_data=nutrient_mass_data
            )
            # Validate to prevent conflicting data being loaded;
            self.validate_nutrient_mass_goal(nutrient_name)
