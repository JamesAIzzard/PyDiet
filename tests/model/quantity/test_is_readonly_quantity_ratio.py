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
