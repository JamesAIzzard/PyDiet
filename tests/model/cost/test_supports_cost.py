from unittest import TestCase

import model


class TestCostPerG(TestCase):
    def setUp(self) -> None:
        self.ingredient = model.ingredients.Ingredient()

    def test_result_is_correct(self):
        self.ingredient.set_cost(
            cost_gbp=1000,
            qty=1,
            unit="kg"
        )
        # noinspection PyPropertyAccess
        self.ingredient.pref_unit = 'g'
        self.assertEqual(self.ingredient.cost_per_g, 1)

        self.ingredient.set_cost(
            cost_gbp=2000,
            qty=1,
            unit="kg"
        )
        # noinspection PyPropertyAccess
        self.ingredient.pref_unit = 'g'
        self.assertEqual(self.ingredient.cost_per_g, 2)


class TestCostPerPrefUnit(TestCase):
    def setUp(self) -> None:
        self.ingredient = model.ingredients.Ingredient()

    def test_result_is_correct(self):
        self.ingredient.set_cost(
            cost_gbp=1,
            qty=1,
            unit="g"
        )
        # noinspection PyPropertyAccess
        self.ingredient.pref_unit = 'kg'
        self.assertEqual(self.ingredient.cost_per_pref_unit, 1000)

        self.ingredient.set_cost(
            cost_gbp=2,
            qty=2,
            unit="kg"
        )
        self.ingredient.pref_unit = 'kg'  # noqa
        self.assertEqual(self.ingredient.cost_per_pref_unit, 1)


class TestCostOfRefQty(TestCase):
    def setUp(self) -> None:
        self.ingredient = model.ingredients.Ingredient()

    def test_result_is_correct(self):
        self.ingredient.set_cost(
            cost_gbp=1,
            qty=1,
            unit="kg"
        )
        # noinspection PyPropertyAccess
        self.ingredient.ref_qty = 100
        # noinspection PyPropertyAccess
        self.ingredient.pref_unit = 'g'
        self.assertEqual(self.ingredient.cost_of_ref_qty, 0.10)

        self.ingredient.set_cost(
            cost_gbp=12.50,
            qty=1,
            unit="kg"
        )
        # noinspection PyPropertyAccess
        self.ingredient.ref_qty = 500
        # noinspection PyPropertyAccess
        self.ingredient.pref_unit = 'g'
        self.assertEqual(self.ingredient.cost_of_ref_qty, 6.25)

        self.ingredient.set_cost(
            cost_gbp=0.00577,
            qty=1,
            unit="g"
        )
        self.ingredient.ref_qty = 100  # noqa
        self.ingredient.pref_unit = 'kg'  # noqa
        self.assertEqual(self.ingredient.cost_of_ref_qty, 577)
