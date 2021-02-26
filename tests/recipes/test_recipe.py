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
