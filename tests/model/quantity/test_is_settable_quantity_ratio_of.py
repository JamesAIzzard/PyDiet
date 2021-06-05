"""Tests for IsSettableQuantityRatioOf class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(isinstance(
            model.quantity.IsSettableQuantityRatioOf(
                subject_qty=model.quantity.IsSettableQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data=qfx.get_qty_data()
                ),
                host_qty=model.quantity.IsSettableQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data=qfx.get_qty_data()
                )
            ),
            model.quantity.IsSettableQuantityRatioOf
        ))

    def test_exception_if_quantity_instances_are_settable(self):
        """Checks we get an exception if we pass in settable quantity instances."""
        with self.assertRaises(AssertionError):
            _ = model.quantity.IsSettableQuantityRatioOf(
                subject_qty=model.quantity.IsReadonlyQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
                ),
                host_qty=model.quantity.IsReadonlyQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
                )
            )


class TestSetQuantity(TestCase):
    """Tests the IsSettableQuantityOf.set_quantity() method in the context of the SettableQuantityRatio class."""

    def test_no_exception_if_subject_qty_less_than_host_qty(self):
        """Checks that we get no exception if the subject quantity is less than the host qty."""
        # Create a test instance;
        isqr = model.quantity.IsSettableQuantityRatioOf(
            subject_qty=model.quantity.IsSettableQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data=qfx.get_qty_data(
                    qty_in_g=10
                )
            ),
            host_qty=model.quantity.IsSettableQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data=qfx.get_qty_data(
                    qty_in_g=20
                )
            )
        )

        # Assert we don't get an exception if we change the value of the subject quantity to
        # something lower than the host quantity.
        isqr.ratio_subject_qty.set_quantity(

        )

    def test_exception_if_subject_qty_greater_than_host_qty(self):
        """Checks that we get an exception if we try to set the subject quantity to a value greater
        than the host quantity."""
        raise NotImplementedError
