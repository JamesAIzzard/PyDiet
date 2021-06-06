"""Tests for IngredientRatioBase"""
from unittest import TestCase, mock

import model.quantity.is_quantity_ratio
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx


class TestGPerSubjectG(TestCase):
    """Tests the ingredient_g_per_subject_g property."""
    def test_correct_value_is_returned(self):
        """Checks we get the correct value back from the property."""
        # Create a test instance with quantities specified;

        irb = ifx.IngredientRatioBaseTestable(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data(for_unique_name=ifx.get_ingredient_name_with(
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
