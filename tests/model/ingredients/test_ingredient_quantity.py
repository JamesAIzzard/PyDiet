"""Tests for the IngredientQuantity class."""
from unittest import TestCase, mock

import model
from tests.model.ingredients import fixtures as fx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_instance_can_be_created(self):
        """Checks that we can create a simple instance without error."""
        self.assertTrue(isinstance(
            model.ingredients.IngredientQuantity(
                ingredient=model.ingredients.Ingredient(
                    ingredient_data_src=fx.get_ingredient_data_src(
                        for_ingredient_name=fx.get_ingredient_name_with("typical_fully_defined_data")
                    )
                ),
                quantity_data_src=qfx.get_qty_data_src(
                    quantity_data=qfx.get_qty_data()
                )
            ),
            model.ingredients.IngredientQuantity
        ))


class TestIngredient(TestCase):
    """Tests the ingredient property."""

    def test_correct_ingredient_is_returned(self):
        """Checks that the correct ingredient instance is returned."""
        # Create a mock ingredient;
        i = mock.Mock()

        # Create an IngredientQuantity, passing the mock ingredient in;
        iq = model.ingredients.IngredientQuantity(
            ingredient=i,
            quantity_data_src=qfx.get_qty_data_src(
                quantity_data=qfx.get_qty_data()
            )
        )

        # Assert the ingredient we get out is the same as we passed in;
        self.assertTrue(i is iq.ingredient)


class TestReqQty(TestCase):
    """Tests the ref_qty property in the context of ingredient."""
    def test_returns_correct_ref_qty(self):
        """Checks that the method returns the correct reference quantity."""
        # Create an IngredientQuantity, passing quantity data in;
        # Create an IngredientQuantity, passing the mock ingredient in;
        iq = model.ingredients.IngredientQuantity(
            ingredient=mock.Mock(),
            quantity_data_src=qfx.get_qty_data_src(
                quantity_data=qfx.get_qty_data(
                    qty_in_g=120,
                    pref_unit="lb"
                )
            )
        )

        # Assert that the correct reference quantity is returned;
        self.assertAlmostEqual(0.2646, iq.ref_qty, delta=0.001)
