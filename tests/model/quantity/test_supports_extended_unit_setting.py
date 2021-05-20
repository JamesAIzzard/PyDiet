"""Tests for SupportsExtendedUnitsSetting class."""
from unittest import TestCase

import model.quantity
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):
    """Tests for the class constructor."""

    def test_can_be_instantiated(self):
        """Check that the instance can be instantiated."""
        self.assertTrue(
            isinstance(model.quantity.SupportsExtendedUnitSetting(),
                       model.quantity.SupportsExtendedUnitSetting)
        )

    def test_data_provided_is_loaded(self):
        """Check that any data provided gets loaded into the instance."""
        # Create the instance first;
        seus = model.quantity.SupportsExtendedUnitSetting(
            extended_units_data=fx.get_extended_units_data(
                g_per_ml=1.2, piece_mass_g=150
            )
        )

        # Check that we get the posted values back;
        self.assertEqual(1.2, seus.g_per_ml)
        self.assertEqual(150, seus.piece_mass_g)


# noinspection PyPep8Naming
class Test_GPerMl(TestCase):
    """Tests for the _g_per_ml property."""

    def test_returns_float_if_defined(self):
        """Returns float if value is set."""
        # Create instance;
        seus = model.quantity.SupportsExtendedUnitSetting(fx.get_extended_units_data(g_per_ml=1.2))

        # Check we get the value back;
        self.assertEqual(1.2, seus._g_per_ml)

    def test_returns_none_if_undefined(self):
        """Returns None if value is not set."""
        # Create instance;
        seus = model.quantity.SupportsExtendedUnitSetting(fx.get_extended_units_data())

        # Check we get None back;
        self.assertEqual(None, seus._g_per_ml)


# noinspection PyPep8Naming
class Test_PieceMassG(TestCase):
    """Tests for the _peice_mass_g property."""

    def test_returns_float_if_defined(self):
        """Returns float if value is set."""
        # Create instance;
        seus = model.quantity.SupportsExtendedUnitSetting(fx.get_extended_units_data(piece_mass_g=150))

        # Check we get the value back;
        self.assertEqual(150, seus._piece_mass_g)

    def test_returns_none_if_undefined(self):
        """Returns None if value is not set."""
        # Create instance;
        seus = model.quantity.SupportsExtendedUnitSetting(fx.get_extended_units_data())

        # Check we get None back;
        self.assertEqual(None, seus._piece_mass_g)


class TestGPerMl(TestCase):
    """Tests the g_per_ml setter."""

    def test_sets_value_correctly(self):
        """Check that a valid value is set correctly."""
        # Create the test instance;
        seus = model.quantity.SupportsExtendedUnitSetting()

        # Check nothing is set;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = seus.g_per_ml

        # Set the value;
        seus.g_per_ml = 1.2

        # Check it was set properly;
        self.assertEqual(1.2, seus.g_per_ml)

    def test_sets_none_correctly(self):
        """Make sure we can pass in None to unset the value."""
        # Create a test instance, passing in a value;
        seus = model.quantity.SupportsExtendedUnitSetting(fx.get_extended_units_data(g_per_ml=1.2))

        # Check we have the value;
        self.assertEqual(1.2, seus.g_per_ml)

        # Now set to None;
        seus.g_per_ml = None

        # Now check it is unset;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = seus.g_per_ml

    def test_raises_exception_if_value_invalid(self):
        """Check we get an exception if the value is invalid."""
        raise NotImplementedError


class TestPieceMassG(TestCase):
    """Tests the piece_mass_g setter."""

    def test_sets_value_correctly(self):
        """Check that a valid value is set correctly."""
        # Create the test instance;
        seus = model.quantity.SupportsExtendedUnitSetting()

        # Check nothing is set;
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            _ = seus.piece_mass_g

        # Set the value;
        seus.piece_mass_g = 150

        # Check it was set properly;
        self.assertEqual(150, seus.piece_mass_g)

    def test_sets_none_correctly(self):
        """Make sure we can pass in None to unset the value."""
        # Create a test instance, passing in a value;
        seus = model.quantity.SupportsExtendedUnitSetting(fx.get_extended_units_data(piece_mass_g=150))

        # Check we have the value;
        self.assertEqual(150, seus.piece_mass_g)

        # Now set to None;
        seus.piece_mass_g = None

        # Now check it is unset;
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            _ = seus.piece_mass_g

    def test_raises_exception_if_value_invalid(self):
        """Check we get an exception if the value is invalid."""
        raise NotImplementedError


class TestLoadData(TestCase):
    """Tests for the load data method."""

    def test_no_error_if_dict_has_no_extended_units_key(self):
        """Check that we don't get an exception if the dict has not extended units key."""
        # Create a test instance;
        seus = model.quantity.SupportsExtendedUnitSetting()

        # Check we get no error if we load an empty dict;
        seus.load_data({})
