"""Tests for the ReadonlyIngredientRatio class."""
from unittest import TestCase, mock

import model
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests for the constructor function."""

    def test_can_create_instance(self):
        """Check we can create an instance."""
        self.assertTrue(isinstance(
            model.ingredients.ReadonlyIngredientRatio(
                ingredient=model.ingredients.ReadonlyIngredient(
                    ingredient_data_src=model.ingredients.get_ingredient_data_src(
                        for_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data"))
                ),
                ratio_host=mock.Mock(),
                qty_ratio_data_src=qfx.get_qty_ratio_data_src(qty_ratio_data=qfx.get_qty_ratio_data())
            ),
            model.ingredients.ReadonlyIngredientRatio
        ))
