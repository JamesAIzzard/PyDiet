from typing import List, Optional

import goals
import model
import persistence


class MealGoalsData(goals.GoalsData):
    """Data Dictionary for MealGoals class."""
    name: Optional[str]
    time: str
    tags: List[str]


class MealGoals(
    goals.HasSettableGoals,
    model.tags.HasSettableTags,
    persistence.HasPersistableData,
    model.HasSettableName
):
    """Models a set of nutrient goals associated with a single meal."""

    def __init__(self, meal_goals_data: Optional['MealGoalsData'] = None, **kwargs):
        super().__init__(**kwargs)

        self._time: Optional[str] = None
        self._parent_day_goal: Optional['goals.DayGoals'] = None

        # Load any data that was provided;
        if meal_goals_data is not None:
            self.load_data(meal_goals_data)

    @property
    def time(self) -> Optional[str]:
        """Returns the serve time_str for the MealGoals instance."""
        if self._time is None:
            raise goals.exceptions.UndefinedMealTimeError(subject=self)
        return self._time

    @time.setter
    def time(self, time: Optional[str]) -> None:
        """Sets the time_str on the MealGoals instance."""
        if time is None:
            self._time = None
        else:
            self._time = model.time.validation.validate_time(time)

    @property
    def parent_day_goal(self) -> 'goals.DayGoals':
        """Returns the DayGoals instance to which this MealGoals instance is associated."""
        if self._parent_day_goal is None:
            raise goals.exceptions.UndefinedParentDayGoalError(subject=self)
        else:
            return self._parent_day_goal

    @parent_day_goal.setter
    def parent_day_goal(self, parent_day_goal: Optional['goals.DayGoals']) -> None:
        """Sets the DayGoals instance to which this MealGoals instance is associated."""
        self._parent_day_goal = parent_day_goal

    def validate_nutrient_mass_goal(self, nutrient_name: str) -> None:
        """Extends the default implementation to trigger the parent's validation, if a parent is attached."""
        # First, check there are no local conflicts;
        super().validate_nutrient_mass_goal(nutrient_name)

        # If we have a parent, then trigger its validation now;
        try:
            self.parent_day_goal.validate_nutrient_mass_goal(nutrient_name)
        # If there is no parent DayGoal, don't worry;
        except goals.exceptions.UndefinedParentDayGoalError:
            pass

    @property
    def persistable_data(self) -> 'MealGoalsData':
        # Grab the data from the superclasses;
        data = super().persistable_data

        # Now add in the data from this class;
        data['time_str'] = self._time

        # Return the data;
        return data

    def load_data(self, data: 'MealGoalsData') -> None:
        super().load_data(data)
        # Load the meal time_str in;
        self.time = data["time_str"]


class PersistableMealGoals(MealGoals, persistence.SupportsPersistence, model.HasSettableName):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    @staticmethod
    def get_path_into_db() -> str:
        return persistence.configs.meal_goals_db_path
