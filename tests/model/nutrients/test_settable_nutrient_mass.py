"""Tests the SettableNutrientMass class."""
from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestConstructor(TestCase):
    """Tests the constructor function."""
    @fx.use_test_nutrients
    def test_can_construct_instance(self):
        """Checks that we can initialise a simple instance."""
        snm = model.nutrients.SettableNutrientMass("tirbur")
        self.assertTrue(isinstance(snm, model.nutrients.SettableNutrientMass))

    @fx.use_test_nutrients
    def test_loads_data_correctly(self):
        """Checks that data we pass in during initialisation gets loaded."""
        # Create a test instance, passing data in;
        snm = model.nutrients.SettableNutrientMass(
            nutrient_name="tirbur",
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=1.2,
                pref_unit="mg"
            )
        )

        # Assert the data ended up on the isntance;
        self.assertEqual(1.2, snm._quantity_data['quantity_in_g'])
        self.assertEqual("mg", snm._quantity_data['pref_unit'])


class TestNutrient(TestCase):
    """Tests the nutrient property."""
    @fx.use_test_nutrients
    def test_correct_nutrient_returned(self):
        """Checks that the correct nutrient instance is returned."""
        # Create a test instance for a specific nutrient;
        snm = model.nutrients.SettableNutrientMass("tirbur")

        # Assert the nutrient property returns the correct nutrient instance;
        self.assertTrue(snm.nutrient is model.nutrients.GLOBAL_NUTRIENTS["tirbur"])