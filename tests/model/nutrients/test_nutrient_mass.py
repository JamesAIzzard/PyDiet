"""Tests for NutrientMass class"""
from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor method."""

    @fx.use_test_nutrients
    def test_can_init_instance(self):
        """Test we can initialise an empty instance."""
        # Create an empty instance;
        nm = model.nutrients.NutrientMass(
            nutrient_name="tirbur",
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
        )
        # Assert it is the right type;
        self.assertTrue(isinstance(nm, model.nutrients.NutrientMass))

    @fx.use_test_nutrients
    def test_can_init_instance_with_data(self):
        """Test we can initialise an instance with data provided."""
        # Create an empty instance;
        nm = model.nutrients.NutrientMass(
            nutrient_name="tirbur",
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(
                qty_in_g=0.12,
                pref_unit="mg"
            ))
        )
        # Assert it is the right type;
        self.assertTrue(isinstance(nm, model.nutrients.NutrientMass))


class TestNutrient(TestCase):
    """Tests the nutrient property."""
    @fx.use_test_nutrients
    def test_nutrient_is_correct(self):
        """Check the nutrient property returns the correct nutrient."""
        # Create a test instance with a named nutrient;
        nm = model.nutrients.NutrientMass(
            nutrient_name="tirbur",
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
        )
        # Assert that the nutrient property returns the correct global nutrient;
        self.assertTrue(nm.nutrient is fx.GLOBAL_NUTRIENTS["tirbur"])