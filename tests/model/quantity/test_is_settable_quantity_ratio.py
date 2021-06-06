"""Tests for IsSettableQuantityRatioOf class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(isinstance(
            model.quantity.IsSettableQuantityRatio(
                ratio_subject=mock.Mock(),
                ratio_host=mock.Mock(),
                qty_ratio_data=qfx.get_qty_ratio_data()
            ),
            model.quantity.IsSettableQuantityRatio
        ))


class TestSetQuantity(TestCase):
    """Tests the IsSettableQuantityOf.set_quantity() method in the context of the SettableQuantityRatio class."""

    def test_no_exception_if_subject_qty_less_than_host_qty(self):
        """Checks that we get no exception if the subject quantity is less than the host qty."""
        # Create a test instance;
        isqr = model.quantity.IsSettableQuantityRatio(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            qty_ratio_data=qfx.get_qty_ratio_data()
        )

        # Assert we don't get an exception if we change the value of the subject quantity to
        # something lower than the host quantity.
        isqr.set_quantity_ratio(
            subject_quantity_value=1,
            subject_quantity_unit='0.1',
            host_quantity_value=110,
            host_quantity_unit="g"
        )

    def test_exception_if_subject_qty_greater_than_host_qty(self):
        """Checks that we get an exception if we try to set the subject quantity to a value greater
        than the host quantity."""
        # Create a test instance;
        isqr = model.quantity.IsSettableQuantityRatio(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            qty_ratio_data=qfx.get_qty_ratio_data()
        )

        # Assert we do get an exception if we change the value of the subject quantity to
        # something greater than the host quantity.
        isqr.set_quantity_ratio(
            subject_quantity_value=1,
            subject_quantity_unit='kg',
            host_quantity_value=100,
            host_quantity_unit="mg"
        )
