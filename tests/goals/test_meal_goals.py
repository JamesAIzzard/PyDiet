from unittest import TestCase

import goals
import tests


class TestConstructor(TestCase):

    def test_creates_instance(self) -> None:
        mg = goals.MealGoals()
        self.assertTrue(isinstance(mg, goals.MealGoals))


class TestName(TestCase):

    def test_name_can_be_set(self) -> None:
        mg = goals.MealGoals()
        mg.name = "Running Breakfast"
        self.assertEqual(mg.name, "Running Breakfast")


class SetNutrientMassGoal(TestCase):

    def test_nutrient_goal_can_be_set_in_g(self) -> None:
        mg = goals.MealGoals()
        mg = tests.goals.fixtures.set_18_g_protein_goal(mg)
        self.assertTrue(mg._nutrient_mass_targets["protein"].nutrient_mass_g == 18)

    def test_nutrient_target_can_be_set_in_kg(self) -> None:
        mg = goals.MealGoals()
        mg.set_nutrient_mass_goal(
            nutrient_name="protein",
            nutrient_mass=0.18,
            nutrient_mass_unit='kg'
        )
        self.assertTrue(mg._nutrient_mass_targets["protein"].nutrient_mass_g == 180)


class UnsetNutrientTarget(TestCase):

    def test_nutrient_target_can_be_deleted(self) -> None:
        # Init meal goals;
        mg = goals.MealGoals()
        # Set protein mass;
        mg = tests.goals.fixtures.set_18_g_protein_goal(mg)
        # Check mass was set;
        self.assertTrue(mg._nutrient_mass_targets["protein"].nutrient_mass_g == 18)
        # Unset protein mass goal;
        mg.unset_nutrient_mass_goal("protein")
        # Check protein is unset;
        self.assertTrue(mg.get_nutrient_mass_goal("protein") is None)
