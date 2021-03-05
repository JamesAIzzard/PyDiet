from unittest import TestCase

from model import recipes


class TestConstructor(TestCase):

    def test_creates_fresh_recipe_instance(self) -> None:
        r = recipes.Recipe()
        self.assertTrue(isinstance(r, recipes.Recipe))


class TestName(TestCase):
    def setUp(self) -> None:
        self.recipe = recipes.Recipe()

    def test_name_sets_and_gets_correctly(self) -> None:
        self.assertEqual(self.recipe.name, None)
        self.recipe.name = "Orange Juice"
        self.assertEqual(self.recipe.name, "Orange Juice")


class TestAddIngredientAmount(TestCase):
    def setUp(self):
        self.recipe = recipes.Recipe()

    def test_ingredient_ratio_can_be_added(self) -> None:
        self.recipe.add_ingredient_ratio(
            ingredient_name="Cucumber",
            ingredient_nominal_quantity=100,
            quantity_units='g',
            inc_perc=10,
            dec_perc=10
        )
        self.assertTrue("Cucumber" in self.recipe.ingredient_names)