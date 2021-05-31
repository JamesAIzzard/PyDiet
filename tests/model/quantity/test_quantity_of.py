"""Tests for the QuantityOf class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):
    """Tests for the constructor method."""

    def test_correct_instance_returned(self):
        """Check that we can instantiate an instance."""
        self.assertTrue(
            isinstance(
                model.quantity.HasReadonlyQuantityOf(
                    subject=mock.Mock(),
                    quantity_data_src=fx.get_qty_data_src(
                        fx.get_qty_data()
                    )
                ),
                model.quantity.HasReadonlyQuantityOf
            )
        )
