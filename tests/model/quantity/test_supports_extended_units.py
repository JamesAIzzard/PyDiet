"""Tests for SupportsExtendedUnits base class.
"""
from unittest import TestCase

import model
from tests.model.quantity import fixtures as fx


class TestGPerMl(TestCase):
    """Tests for the g_per_ml property."""

    def test_returns_g_per_ml_if_defined(self):
        """Checks we get the grams per ml value returned if it is defined."""
        # Create a testable instance;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.1)

        # Assert that the value is returned;
        self.assertEqual(1.1, seu.g_per_ml)

    def test_raises_exception_if_not_defined(self):
        """Checks we get an exception if g_per_ml is not defined."""
        # Create a testable instance;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=None)

        # Assert we get an error if we try and call g_per_ml;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = seu.g_per_ml
