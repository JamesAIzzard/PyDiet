"""Tests for the HasSettableIngredientQuantities class."""
from unittest import TestCase

import model

from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_simple_instance(self):
        """Checks we can construct a simple instance."""
        self.assertTrue(isinstance(model.ingredients.HasSettableIngredientQuantities(),
                                   model.ingredients.HasSettableIngredientQuantities))

    def test_supplied_data_is_loaded_correctly(self):
        """Checks that any data we pass in gets loaded correctly."""
        # Create some test data;
        iq_data = {
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        }

        # Create a test instance, passing this data in;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data=iq_data)

        # Check the data was passed in OK;
        self.assertEqual(iq_data, hsiq.persistable_data['ingredient_quantities_data'])
