"""Defines tests for the BaseRatioOf class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestNumeratorGPerDenominatorG(TestCase):
    """Tests the numerator_g_per_denominator_g property."""

    def test_correct_value_is_returned(self):
        """Checks that we get the correct value back."""
        # Create a test instance with numerator and denominator quantities defined;
        bro = qfx.HasReadableRatioOfTestable(
            numerator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=10))
            ),
            denominator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=20))
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(0.5, bro.numerator_g_per_denominator_g)


class TestNumeratorMassInPrefUnitPerGOfDenominator(TestCase):
    """Tests the numerator_mass_in_pref_unit_per_g_of_denominator property."""

    def test_correct_value_is_returned(self):
        """Checks that the property returns the correct value."""
        # OK, lets simulate a ratio with 10mg of x for every 40g of y.
        # Create a testable instance to represent this scenario;
        bro = qfx.HasReadableRatioOfTestable(
            numerator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=0.01, pref_unit='mg'))
            ),
            denominator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(0.25, bro.numerator_mass_in_pref_unit_per_g_of_denominator)


class TestNumeratorMassInPrefUnitPerRefQtyOfDenominator(TestCase):
    """Tests the numerator_mass_in_pref_unit_per_ref_qty_of_denominator property."""

    def test_correct_value_is_returned(self):
        """Checks that the property returns the correct value."""
        # Create a test instance with 10mg of x per 40g of y
        bro = qfx.HasReadableRatioOfTestable(
            numerator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=0.01, pref_unit='mg'))
            ),
            denominator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(10, bro.numerator_mass_in_pref_unit_per_ref_qty_of_denominator)


class TestRatioIsDefined(TestCase):
    """Tests the ratio_is_defined property."""

    def test_returns_true_if_ratio_is_defined(self):
        """Checks that the property returns True if the ratio is defined."""
        # Create a fully defined test instance;
        bro = qfx.HasReadableRatioOfTestable(
            numerator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=0.01, pref_unit='mg'))
            ),
            denominator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we the property returns True;
        self.assertTrue(bro.ratio_is_defined)

    def test_returns_false_if_ratio_is_undefined(self):
        """Checks that the property returns False if the ratio is undefined."""
        # Create a partially undefined test instance;
        bro = qfx.HasReadableRatioOfTestable(
            numerator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=None, pref_unit='mg'))
            ),
            denominator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we the property returns False;
        self.assertFalse(bro.ratio_is_defined)


class TestPersistableData(TestCase):
    """Tests the persistable data property."""

    def test_returns_correct_data(self):
        """Checks that the property returns the correct data."""
        # Create some test data;
        numerator_data = qfx.get_qty_data(qty_in_g=10, pref_unit="g")
        denominator_data = qfx.get_qty_data(qty_in_g=200, pref_unit="kg")

        # Create a test instance, passing in the test data;
        bro = qfx.HasReadableRatioOfTestable(
            numerator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(numerator_data)
            ),
            denominator=model.quantity.HasReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(denominator_data)
            )
        )

        # Assert that the data we get back, is the same data that went in;
        self.assertEqual(
            model.quantity.RatioData(
                numerator_qty_data=numerator_data,
                denominator_qty_data=denominator_data
            ),
            bro.persistable_data
        )
