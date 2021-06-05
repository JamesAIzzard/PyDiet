"""Tests for IsReadonlyQuantityRatioOf class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(isinstance(
            model.quantity.IsReadonlyQuantityRatioOf(
                subject_qty=model.quantity.IsReadonlyQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
                ),
                host_qty=model.quantity.IsReadonlyQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
                )
            ),
            model.quantity.IsReadonlyQuantityRatioOf
        ))

    def test_exception_if_quantity_instances_are_settable(self):
        """Checks we get an exception if we pass in settable quantity instances."""
        with self.assertRaises(AssertionError):
            _ = model.quantity.IsReadonlyQuantityRatioOf(
                subject_qty=model.quantity.IsSettableQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data=qfx.get_qty_data()
                ),
                host_qty=model.quantity.IsSettableQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data=qfx.get_qty_data()
                )
            )
