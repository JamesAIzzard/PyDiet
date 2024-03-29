"""Tests for IngredientRatioBase"""
from unittest import TestCase, mock

import model.quantity.is_quantity_ratio
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests the constructor function."""
    def test_exception_if_subject_not_ingredient(self):
        """Checks that we get an exception if the subject isnt an ingredient."""
        # Check we get an exception if we try to instantiate with something
        # other than an ingredient.
        with self.assertRaises(TypeError):
            _ = ifx.IngredientRatioBaseTestable(
                ingredient=mock.Mock(),
                host=mock.Mock(),
                qty_ratio_data=qfx.get_qty_ratio_data()
            )


class TestIngredient(TestCase):
    """Tests the ingredient property."""
    @pfx.use_test_database
    def test_ingredient_returned_correctly(self):
        """Tests that we get the correct ingredient back."""
        # Create a test instance with quantities specified;
        irb = ifx.IngredientRatioBaseTestable(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=model.ingredients.get_ingredient_data_src(for_unique_name="Spinach")
            ),
            host=mock.Mock(),
            qty_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=10,
                host_qty_g=100
            )
        )

        # Assert we get the right ingredient back;
        self.assertEqual("Spinach", irb.ingredient.name)
        self.assertTrue(isinstance(irb.ingredient, model.ingredients.ReadonlyIngredient))


class TestGPerSubjectG(TestCase):
    """Tests the g_per_subject_g property."""
    def test_correct_value_is_returned(self):
        """Checks we get the correct value back from the property."""
        # Create a test instance with quantities specified;
        irb = ifx.IngredientRatioBaseTestable(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(for_unique_name=ifx.get_ingredient_name_with(
                    "typical_fully_defined_data"
                ))
            ),
            host=mock.Mock(),
            qty_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=10,
                host_qty_g=100
            )
        )

        # Assert that we get the right ratio back;
        self.assertEqual(0.1, irb.subject_g_per_host_g)
