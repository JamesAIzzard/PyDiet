from typing import Optional, List, Dict

import goals
import model
import persistence


class DayGoalsData(goals.GoalsData):
    name: Optional[str]
    meal_goals: Dict[str, 'goals.MealGoalsData']


class DayGoals(goals.HasSettableGoals, persistence.SupportsPersistence, model.HasSettableName):
    """Models a set of nutrient goals associated with a day.
    A DayGoals instance may have its own set of goals, and also a collection of MealGoals instances
    which my have their own sets of goals.
    Notes:
        Part of the validation task here is to ensure the DayGoals data and the associated MealGoals data
        cannot be set into a conflicting state.
    """

    def __init__(self, day_goals_data: Optional['DayGoalsData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._meal_goals: Dict[str, 'goals.MealGoals'] = {}

        # Load any data that is provided;
        if day_goals_data is not None:
            self.load_data(day_goals_data)

    @model.HasSettableName.name.setter
    def name(self, name: Optional[str]) -> None:
        # Extend to check for uniqueness, since we are using the name as the unique value;
        # If the name is None, we are unsetting, so not worried, crack on;
        if name is None:
            super().name = None

        # Otherwise, check the name is unique;
        super().name = self.validate_unique_value(name)

    @property
    def unique_value(self) -> str:
        # We are using the name as the unique value here;
        try:
            return self.name
        # If we get an undefined name error, convert it to an undefined unique value error.
        except model.exceptions.UndefinedNameError:
            raise persistence.exceptions.UndefinedUniqueValueError(subject=self)

    def get_total_nutrient_mass_goal_g_from_all_meal_goals(self, nutrient_name: str) -> float:
        """Returns the sum total mass of the nutrient from all attached MealGoal instances."""
        # Init the rolling total;
        rolling_total: float = 0
        # Create a flag to indicate if any MealGoals actually defined the nutrient;
        defined = False
        # Cycle through the mealgoals and try and roll up the total if defined;
        for meal_goal in self.meal_goals.values():
            try:
                rolling_total = rolling_total + meal_goal.get_nutrient_mass_goal(nutrient_name).nutrient_mass_g
                defined = True
            # If not defined, just go onto the next one;
            except goals.exceptions.UndefinedNutrientMassGoalError:
                continue
        # If not a single one was set, then raise an exception;
        if defined is False:
            raise goals.exceptions.UndefinedNutrientMassGoalError(nutrient_name=nutrient_name)
        # Otherwise just return the total;
        return rolling_total

    def validate_nutrient_mass_goal(self, nutrient_name: str) -> None:
        """Extends the local nutrient mass goal validation to check the nutrient mass goal is does not
        conflict with defined family values including those in any attached MealGoals instances.
        """

        # First check there are no conflicts on the locally defined goals;
        super().validate_nutrient_mass_goal(nutrient_name)

        # If we don't have child MealGoals, the can just exit here;
        if len(self.meal_goals) == 0:
            return

        # OK, run the validation but now including values from all the MealGoals.
        _ = model.nutrients.validate_nutrient_family_masses(
            nutrient_name=nutrient_name,
            nutrient_mass_g=self.get_nutrient_mass_goal(nutrient_name).nutrient_mass_g,
            get_nutrient_mass_g=self.get_total_nutrient_mass_goal_g_from_all_meal_goals
        )

    @property
    def meal_goals(self) -> Dict[str, 'goals.MealGoals']:
        """Returns a dict of the MealGoals instances associated with this DayGoals instance."""
        return self._meal_goals

    def add_meal_goals(self, meal_goals: List['goals.MealGoals']) -> None:
        """Adds MealGoals instances to the DayGoals.
        Note:
            Requires that each MealGoals instance has a unique name.
        """
        for meal_goal in meal_goals:
            # Catch absent name;
            if meal_goal.name is None:
                raise goals.exceptions.UndefinedMealGoalNameError(subject=self)
            # Catch duplicated name;
            if meal_goal.name in self._meal_goals.keys():
                raise goals.exceptions.MealGoalNameClashError(subject=self, clashing_name=meal_goal.name)

        # All OK, go ahead and add references and add to list;
        for meal_goal in meal_goals:
            # Place reference to DayGoal in MealGoal
            meal_goal.parent_day_goal = self
            # Add the MealGoal instance;
            self._meal_goals[meal_goal.name] = meal_goal

    def meal_goals_persistable_data(self) -> Dict[str, 'goals.MealGoalsData']:
        """Returns a dict of persistable data for the meal goals instances."""
        data = {}
        for meal_goal_name, meal_goal in self.meal_goals.items():
            data[meal_goal_name] = meal_goal.persistable_data
        return data

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.day_goals_db_path

    @property
    def persistable_data(self) -> 'DayGoalsData':
        # Grab the data from the superclass;
        data = super().persistable_data
        data['meal_goals'] = self.meal_goals_persistable_data
        return data

    def load_data(self, data: 'DayGoalsData') -> None:
        # Load the local goals;
        super().load_data(data)

        # Load in the MealGoals;
        for meal_goal_name, meal_goals_data in data['meal_goals'].items():
            self._meal_goals[meal_goal_name] = goals.MealGoals(meal_goals_data=meal_goals_data)
