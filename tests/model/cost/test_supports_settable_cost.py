from unittest import TestCase

from model import ingredients


class TestCostPerG(TestCase):
    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_property_setter_works(self):
        # noinspection PyPropertyAccess
        self.ingredient.cost_per_g = 0.05


class TestSetCost(TestCase):
    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_set_cost_sets_cost(self):
        self.ingredient.set_cost(
            cost_gbp=12.00,
            qty=2.5,
            unit='kg'
        )
        self.assertEqual(self.ingredient.cost_per_g, 0.0048)
