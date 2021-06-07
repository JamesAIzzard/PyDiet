"""Tests for IsReadonlyQuantityRatio class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(isinstance(
            model.quantity.IsReadonlyQuantityRatio(
                ratio_subject=mock.Mock(),
                ratio_host=mock.Mock(),
                qty_ratio_data_src=qfx.get_qty_ratio_data_src(qty_ratio_data=qfx.get_qty_ratio_data())
            ),
            model.quantity.IsReadonlyQuantityRatio
        ))

    def test_exception_if_subject_qty_greater_than_host_qty(self):
        """Checks that we can't construct an instance where the subject quantity is greater than
        the host quantity."""
        # Assert we get an exception if we try to create a quantity ratio where the
        # subject quantity is greater than the host quantity;
        with self.assertRaises(model.quantity.exceptions.SubjectQtyExceedsHostQtyError):
            _ = model.quantity.IsReadonlyQuantityRatio(
                ratio_subject=mock.Mock(),
                ratio_host=mock.Mock(),
                qty_ratio_data_src=qfx.get_qty_ratio_data_src(qty_ratio_data=qfx.get_qty_ratio_data(
                    subject_qty_g=100,
                    host_qty_g=20
                ))
            )
