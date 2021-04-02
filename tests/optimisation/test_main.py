from unittest import TestCase

import persistence
import goals
from optimisation import optimise_meal_goals
from model import meals


class TestOptimiseMealGoals(TestCase):

    def test_returns_meal_quantity(self) -> None:
        """Checks the function returns a MealQuantity instance."""
        # Load the MealGoals instance
        mg = persistence.load(goals.PersistableMealGoals, unique_value="Test Breakfast")
        # Run the optimisation and grab the result;
        mq = optimise_meal_goals(mg)
        # Check the result is a MealQuantity instance;
        self.assertTrue(isinstance(mq, meals.MealQuantity))
