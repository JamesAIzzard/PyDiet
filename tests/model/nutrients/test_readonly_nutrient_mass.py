"""Tests the ReadonlyNutrientMass class."""
from unittest import TestCase

import model
from tests.model.nutrients import fixtures as nfx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    @nfx.use_test_nutrients
    def test_can_construct_simple_instance(self):
        """Check we can construct a simple instance."""
        self.assertTrue(isinstance(model.nutrients.ReadonlyNutrientMass(
            nutrient_name="foo",
            quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data())
        ),
            model.nutrients.ReadonlyNutrientMass
        ))

    @nfx.use_test_nutrients
    def test_exception_if_nutrient_name_invalid(self):
        """Check we get an exception if the nutrient name is invalid."""
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            _ = model.nutrients.ReadonlyNutrientMass(
                nutrient_name="fake",
                quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data())
            )

    @nfx.use_test_nutrients
    def test_exception_if_qty_is_invalid(self):
        """Check we get an exception if we pass invalid data in."""
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            # noinspection PyTypeChecker
            _ = model.nutrients.ReadonlyNutrientMass(
                nutrient_name="bar",
                quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data(
                    qty_in_g="invalid"
                ))
            )

    @nfx.use_test_nutrients
    def test_exception_if_unit_is_not_mass(self):
        """Check we get an exception if we try to instantiate with a non-mass unit."""
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            _ = model.nutrients.ReadonlyNutrientMass(
                nutrient_name="bar",
                quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data(
                    qty_in_g=10,
                    pref_unit="ml"
                ))
            )


class TestQtySubject(TestCase):
    """Tests the qty_subject method."""

    @nfx.use_test_nutrients
    def test_check_correct_nutrient_is_returned(self):
        """Check we get the correct nutrient back."""
        # Create a test instance of a specified nutrient;
        rnm = model.nutrients.ReadonlyNutrientMass(
            nutrient_name="foo",
            quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data())
        )

        # Check that the qty_subject is the correct global nutrient instance;
        self.assertTrue(rnm.qty_subject is model.nutrients.GLOBAL_NUTRIENTS["foo"])


class TestRefQty(TestCase):
    """Tests the ref_qty method."""

    @nfx.use_test_nutrients
    def test_check_correct_value_is_returned(self):
        """Check we get the correct reference quantity back."""
        # Create a test instance with defined qty;
        rnm = model.nutrients.ReadonlyNutrientMass(
            nutrient_name="foo",
            quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data(
                qty_in_g=100,
                pref_unit="kg"
            ))
        )

        # Check the ref_qty is correct;
        self.assertEqual(0.1, rnm.ref_qty)


class TestNotWritable(TestCase):
    """Tests we can't set the readonly instance."""

    @nfx.use_test_nutrients
    def test_cant_access_setter(self):
        """Check we get an attribute error if we try to access setter."""
        # Create a test instance with defined qty;
        rnm = model.nutrients.ReadonlyNutrientMass(
            nutrient_name="foo",
            quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data())
        )

        # Check we get an exception if we try to set it;
        with self.assertRaises(AttributeError):
            # noinspection PyUnresolvedReferences
            rnm.set_quantity(
                quantity_value=10,
                quantity_unit='g'
            )
