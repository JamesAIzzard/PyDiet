from typing import List, Optional

from model import nutrients, quantity
import persistence
import goals


class MealGoalsData(goals.GoalsData):
    """Data Dictionary for MealGoals class."""
    name: Optional[str]
    time: Optional[str]
    tags: List[str]


class MealGoals(goals.HasSettableGoals):
    """Models a set of nutrient goals associated with a single meal."""

    def __init__(self, meal_goals_data: Optional['MealGoalsData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._name: Optional[str] = None
        self._time: Optional[str] = None
        self._max_cost_gbp_target: Optional[float] = None
        self._calorie_target: Optional[float] = None
        self._parent_day_goal: Optional['goals.DayGoals'] = None

        # Load any data that was provided;
        if meal_goals_data is not None:
            self.load_data(meal_goals_data)

    @property
    def name(self) -> str:
        """Returns the name of the MealGoals instance."""
        return self._name

    @name.setter
    def name(self, name: Optional[str]) -> None:
        self._name = name

    @property
    def time(self) -> Optional[str]:
        """Returns the serve time for the MealGoals instance."""
        return self._time

    @time.setter
    def time(self, time: Optional[str]) -> None:
        """Sets the time on the MealGoals instance."""
        self._time = time

    @property
    def max_cost_gbp_target(self) -> Optional[float]:
        """Returns the target max cost gbp for the MealGoals instance."""
        return self._max_cost_gbp_target

    @max_cost_gbp_target.setter
    def max_cost_gbp_target(self, max_cost_gbp_target: Optional[float]) -> None:
        """Sets the target max cost gbp for the MealGoals instance."""
        self._max_cost_gbp_target = max_cost_gbp_target

    @property
    def calorie_target(self) -> Optional[float]:
        """Returns the calorie target for the MealGoals instance."""
        return self._calorie_target

    @calorie_target.setter
    def calorie_target(self, calorie_target: Optional[float]) -> None:
        """Sets the calorie target for the MealGoals instance."""
        self._calorie_target = calorie_target

    @property
    def parent_day_goal(self) -> 'goals.DayGoals':
        """Returns the DayGoals instance to which this MealGoals instance is associated."""
        return self._parent_day_goal

    @parent_day_goal.setter
    def parent_day_goal(self, parent_day_goal: 'goals.DayGoals') -> None:
        """Sets the DayGoals instance to which this MealGoals instance is associated."""
        self._parent_day_goal = parent_day_goal

    def set_nutrient_mass_goal(self, nutrient_name: str, nutrient_mass: Optional[float] = None,
                               nutrient_mass_unit: str = 'g'):
        """Extends the parent implementation to check that:
        - This nutrient mass does not cause the total across all MealGoals on this DayGoal to exceed
            the target stated on the DayGoals instance.
        - This nutrient mass was not previously unset, and would now cause the DayGoal's instance
            to be overconstrained.
        """

        # If we are unsetting, go ahead, no need to check.
        if nutrient_mass is None:
            super().set_nutrient_mass_goal(nutrient_name, nutrient_mass, nutrient_mass_unit)
            return

        # If we don't have a parent DayGoals, we don't worry about the next checks;
        if self.parent_day_goal is None:
            super().set_nutrient_mass_goal(nutrient_name, nutrient_mass, nutrient_mass_unit)
            return

        # If goal was previously unset, check we don't overconstrain;
        if self.get_nutrient_mass_goal(nutrient_name) is None:
            unconstrained = 0
            for meal_goals in self.parent_day_goal.meal_goals.values():
                if meal_goals.get_nutrient_mass_goal(nutrient_name) is None:
                    unconstrained = unconstrained + 1
            if unconstrained <= 1:
                raise goals.exceptions.OverConstrainedNutrientMassGoalError()

        # Check the new value does not exceed any goal set on the DayGoals instance;
        # Only required if DayGoals specified goal for this nutrient;
        if self.parent_day_goal.get_nutrient_mass_goal(nutrient_name) is not None:
            # Init the total with the proposed new value, and exclude the current value
            # during the accumulation loop;
            goal_total_g: float = quantity.convert_qty_unit(
                qty=nutrient_mass,
                start_unit=nutrient_mass_unit,
                end_unit='g'
            )
            for meal_goals in self.parent_day_goal.meal_goals.values():
                if meal_goals is not self:  # Exclude old total - we started with new total;
                    if meal_goals.get_nutrient_mass_goal(nutrient_name) is not None:
                        goal_total_g = goal_total_g + meal_goals.get_nutrient_mass_goal(nutrient_name, 'g')
            if goal_total_g > self.parent_day_goal.get_nutrient_mass_goal(nutrient_name, 'g'):
                raise goals.exceptions.ConflictingNutrientMassGoalError()

        # All is OK, so defer to super();
        super().set_nutrient_mass_goal(nutrient_name, nutrient_mass, nutrient_mass_unit)

    def load_data(self, meal_goals_data: 'MealGoalsData') -> None:
        """Loads MealGoals data into instance.
        Notes:
            Does not assume key is in dictionary to allow old datafiles to have new keys
            automatically updated if the system is extended.
        """

        # Load in the nutrient name;
        if "name" in meal_goals_data.keys():
            self.name = meal_goals_data["name"]

        # Load in the serve time;
        if "time" in meal_goals_data.keys():
            self.time = meal_goals_data["time"]

        # Load in the max cost gbp target
        if "max_cost_gbp_target" in meal_goals_data.keys():
            self.max_cost_gbp_target = meal_goals_data["max_cost_gbp_target"]

        # Load in the calorie target;
        if "calorie_target" in meal_goals_data.keys():
            self.calorie_target = meal_goals_data["calorie_target"]

        # Load in the nutrient mass goals;
        if "nutrient_mass_goals" in meal_goals_data.keys():
            for nutrient_name in meal_goals_data["nutrient_mass_goals"]:
                nutrient_name = nutrients.validation.validate_nutrient_name(nutrient_name)
                self.set_nutrient_mass_goal(
                    nutrient_name=nutrient_name,
                    nutrient_mass=meal_goals_data["nutrient_mass_goals"][nutrient_name]["nutrient_mass_g"],
                    nutrient_mass_unit='g'
                )


class PersistableMealGoals(MealGoals, persistence.SupportsPersistence):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name(self) -> str:
        """Overrides the local name getter to use the unique value associated with persistence."""
        return self.unique_value

    @name.setter
    def name(self, name: Optional[str]) -> None:
        """Overrides the name setter to deal with the unique value properties used by persistence module."""
        self.unique_value = name

    @property
    def persistable_data(self) -> 'MealGoalsData':
        return MealGoalsData(
            name=self.name,
            time=self.time,
            max_cost_gbp_target=self.max_cost_gbp_target,
            flags={},
            tags=[],
            calorie_target=self.calorie_target,
            nutrient_mass_goals={}
        )

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.meal_goals_db_path
