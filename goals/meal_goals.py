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

        # Load in the nutrient name;
        self._name = meal_goals_data["name"]

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

    def persistable_data(self) -> 'MealGoalsData':
        return MealGoalsData(
            name="...",
            time="##:##",
            max_cost_gbp_target=12.00,
            flags={},
            tags=[],
            calorie_target=600,
            nutrient_mass_goals={}
        )

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.meal_goals_db_path
