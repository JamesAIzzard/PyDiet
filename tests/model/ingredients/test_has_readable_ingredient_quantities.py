"""Tests the HasIngredientQuantities class."""
from unittest import TestCase

import model.ingredients
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx
from tests.persistence import fixtures as pfx


class TestIngredientQuantities(TestCase):
    """Tests the ingredient_quantities property."""

    def test_correct_quantity_types_returned(self):
        """Checks we get a set of correctly named ReadonlyIngredientQuantities returned."""
        # Create a test instance, with some ingredients;
        hriq = ifx.HasReadableIngredientQuantitiesTestable(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Check each ingredient quantity is of the correct type;
        for iq in hriq.ingredient_quantities.values():
            self.assertTrue(isinstance(iq, model.ingredients.ReadonlyIngredientQuantity))
            self.assertFalse(isinstance(iq, model.ingredients.SettableIngredientQuantity))

    def test_correct_number_instances_are_returned(self):
        """Checks that we get the correct number of ingredient quantity instances."""
        # Create a test instance, with some ingredients;
        hriq = ifx.HasReadableIngredientQuantitiesTestable(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Check the method returns the correct number of instances;
        self.assertEqual(3, len(hriq.ingredient_quantities))

    def test_instances_have_correct_data(self):
        """Checks that the ReadonlyIngredientQuantity instances which get returned are loaded with
        the correct data."""
        # Create a test instance, with some ingredients;
        hriq = ifx.HasReadableIngredientQuantitiesTestable(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Grab the return values from the method;
        iqs = hriq.ingredient_quantities

        # Check that we have the correct quantities of each ingredient;
        self.assertEqual(100, iqs[ifx.get_ingredient_df_name("Raspberry")].quantity_in_g)
        self.assertEqual(110, iqs[ifx.get_ingredient_df_name("Aubergine")].quantity_in_g)
        self.assertEqual(120, iqs[ifx.get_ingredient_df_name("Lemon Juice")].quantity_in_g)


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

