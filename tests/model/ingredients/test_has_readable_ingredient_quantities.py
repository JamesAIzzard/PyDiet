"""Tests the HasIngredientQuantities class."""
from unittest import TestCase

import model.ingredients
import persistence
from tests.model.ingredients import fixtures as ifx
from tests.persistence import fixtures as pfx
from tests.model.quantity import fixtures as qfx


class TestIngredientUniqueNames(TestCase):
    """Tests the ingredient names property."""

    @pfx.use_test_database
    def test_correct_names_are_returned(self):
        """Checks the method returns the correct list of names."""
        # Create a test instance, with some ingredients;
        hiq = ifx.HasReadableIngredientQuantitiesTestable(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Assert the correct list of ingredient names are returned;
        self.assertEqual({"Raspberry", "Aubergine", "Lemon Juice"}, set(hiq.ingredient_unique_names))


class TestPersistableData(TestCase):
    """Tests the persistable data property."""
    def test_data_dict_contains_correct_data(self):
        """Checks the persistable data dict contains the correct data."""
        # Create some test data;
        iq_data = {
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        }

        # Create a test instance, with some ingredients;
        hiq = ifx.HasReadableIngredientQuantitiesTestable(ingredient_quantities_data=iq_data)

        # Grab the persistable data;
        data = hiq.persistable_data

        # Check the persistable data dict contains the correct heading, with the correct data;
        self.assertTrue('ingredient_quantities_data' in hiq.persistable_data.keys())

        # Check the data dict is the same as the one we passed in;
        self.assertEqual(iq_data, hiq.persistable_data['ingredient_quantities_data'])

