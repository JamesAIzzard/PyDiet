from unittest import TestCase

from model import goals
import tests


def configure_basic_meal_goals(day_goals: 'goals.DayGoals') -> 'goals.DayGoals':
    """Configues basic meal goals on the day goals instance for use in tests."""
    # Configure some day goals;
    day_goals.add_meal_goals([
        goals.MealGoals({
            "name": "Breakfast",
            "nutrient_mass_goals": {
                "protein": {
                    "nutrient_mass_g": 40
                }
            }
        }),
        goals.MealGoals({
            "name": "Lunch",
            "nutrient_mass_goals": {
                "protein": {
                    "nutrient_mass_g": 45
                }
            }
        }),
        goals.MealGoals({
            "name": "Dinner",
            "nutrient_mass_goals": {
                "protein": {
                    "nutrient_mass_g": 50
                }
            }
        })
    ])

    return day_goals


class TestConstructor(TestCase):

    def test_creates_instance(self) -> None:
        dg = goals.DayGoals()
        self.assertTrue(isinstance(dg, goals.DayGoals))


class TestName(TestCase):
    def test_name_can_be_set(self) -> None:
        dg = goals.DayGoals()
        dg.name = "Rest Day"
        self.assertEqual(dg.name, "Rest Day")


class SetNutrientMassGoal(TestCase):
    def test_nutrient_goal_can_be_set_in_g(self) -> None:
        dg = goals.DayGoals()
        dg = tests.goals.fixtures.set_18_g_protein_goal(dg)
        self.assertTrue(dg._nutrient_mass_targets["protein"].nutrient_mass_g == 18)

    def test_nutrient_target_can_be_set_in_kg(self) -> None:
        dg = goals.DayGoals()
        dg.set_nutrient_mass_goal(
            nutrient_name="protein",
            nutrient_mass=0.18,
            nutrient_mass_unit='kg'
        )
        self.assertTrue(dg._nutrient_mass_targets["protein"].nutrient_mass_g == 180)

    def test_raises_exception_if_day_goal_nutrient_mass_target_set_lower_than_child_meal_goals_total(self) -> None:
        """Check we get an exception if we try to set a nutrient target on the DayGoal
        lower than the sum of the values on its child MealGoals, or vice-versa.
        """
        dg = goals.DayGoals()
        # Configure some child meal goals;
        dg = configure_basic_meal_goals(dg)
        # Add another so we can set without overconstraining;
        dg.add_meal_goals([goals.MealGoals({"name": "Snack"})])
        # Try and set the protein target on the day goals to less than the sum
        # of protein on the meal goals;
        with self.assertRaises(goals.exceptions.ConflictingNutrientMassGoalError):
            dg.set_nutrient_mass_goal("Protein", 50, 'g')

    def test_raises_exception_if_child_meal_goals_nutrient_mass_target_set_to_exceed_parent_total(self) -> None:
        """Check we get an exception if we set a child MealGoals nutrient mass target which causes
        the total child MealGoals target for that nutrient to exceed the stated total on the parent
        DayGoals instance."""
        dg = goals.DayGoals()
        dg.set_nutrient_mass_goal("Protein", 80, 'g')
        breakfast = goals.MealGoals({"name": "Breakfast"})
        lunch = goals.MealGoals({"name": "Lunch"})
        dg.add_meal_goals([breakfast, lunch])

        with self.assertRaises(goals.exceptions.ConflictingNutrientMassGoalError):
            breakfast.set_nutrient_mass_goal("Protein", 90, 'g')

    def test_raises_exception_when_setting_nutrient_target_when_nutrient_constrained_by_meal_goals(self) -> None:
        """Check we can't overconstrain the DayGoals instance by setting a nutrient target when
        each of its child MealGoals already has that nutrients target completely specified."""
        dg = goals.DayGoals()
        dg = configure_basic_meal_goals(dg)
        with self.assertRaises(goals.exceptions.OverConstrainedNutrientMassGoalError):
            dg.set_nutrient_mass_goal("Protein", 180, 'g')

class TestAddMealGoals(TestCase):

    def test_dissallow_adding_of_unnamed_meal_goals(self) -> None:
        """Check we get an exception if we try and add an unnamed MealGoals instance."""
        dg = goals.DayGoals()
        mg = goals.MealGoals()
        with self.assertRaises(goals.exceptions.UnnamedMealGoalError):
            dg.add_meal_goals([mg])