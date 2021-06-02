"""Tests for SupportsExtendedUnitsSetting class."""
from unittest import TestCase

import model.quantity
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):
    """Tests for the class constructor."""

    def test_can_be_instantiated(self):
        """Check that the instance can be instantiated."""
        self.assertTrue(
            isinstance(model.quantity.HasSettableExtendedUnits(),
                       model.quantity.HasSettableExtendedUnits)
        )

    def test_data_provided_is_loaded(self):
        """Check that any data provided gets loaded into the instance."""
        # Create the instance first;
        seus = model.quantity.HasSettableExtendedUnits(
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
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data(g_per_ml=1.2))

        # Check we get the value back;
        self.assertEqual(1.2, seus._g_per_ml)

    def test_returns_none_if_undefined(self):
        """Returns None if value is not set."""
        # Create instance;
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data())

        # Check we get None back;
        self.assertEqual(None, seus._g_per_ml)


# noinspection PyPep8Naming
class Test_PieceMassG(TestCase):
    """Tests for the _peice_mass_g property."""

    def test_returns_float_if_defined(self):
        """Returns float if value is set."""
        # Create instance;
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data(piece_mass_g=150))

        # Check we get the value back;
        self.assertEqual(150, seus._piece_mass_g)

    def test_returns_none_if_undefined(self):
        """Returns None if value is not set."""
        # Create instance;
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data())

        # Check we get None back;
        self.assertEqual(None, seus._piece_mass_g)


class TestGPerMl(TestCase):
    """Tests the g_per_ml setter."""

    def test_sets_value_correctly(self):
        """Check that a valid value is set correctly."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

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
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data(g_per_ml=1.2))

        # Check we have the value;
        self.assertEqual(1.2, seus.g_per_ml)

        # Now set to None;
        seus.g_per_ml = None

        # Now check it is unset;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = seus.g_per_ml

    def test_raises_exception_if_value_invalid(self):
        """Check we get an exception if the value is invalid."""
        # Create test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we try to set an invalid value;
        # Try with string;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.g_per_ml = "invalid"
        # Try with negative value;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.g_per_ml = -4
        # Try with zero;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.g_per_ml = 0


class TestPieceMassG(TestCase):
    """Tests the piece_mass_g setter."""

    def test_sets_value_correctly(self):
        """Check that a valid value is set correctly."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

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
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data(piece_mass_g=150))

        # Check we have the value;
        self.assertEqual(150, seus.piece_mass_g)

        # Now set to None;
        seus.piece_mass_g = None

        # Now check it is unset;
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            _ = seus.piece_mass_g

    def test_raises_exception_if_value_invalid(self):
        """Check we get an exception if the value is invalid."""
        # Create test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we try to set an invalid value;
        # Try with string;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.piece_mass_g = "invalid"
        # Try with negative value;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.piece_mass_g = -5
        # Try with zero;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.piece_mass_g = 0


class TestSetDensity(TestCase):
    """Tests for the set_density method."""

    def test_sets_density_correctly(self):
        """Check the density can be set with arbitrary units correctly."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check the density is not configured;
        self.assertFalse(seus.density_is_defined)

        # Set the density;
        seus.set_density(
            mass_qty=1.5,
            mass_unit='kg',
            vol_qty=2,
            vol_unit="L"
        )

        # Assert the density was set correctly;
        self.assertEqual(0.75, seus.g_per_ml)

    def test_raises_exception_if_value_is_none(self):
        """Check that we can't pass None values into this method. We
        should be using the unset_density method to unset the instance's density."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we pass in None to both;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            # noinspection PyTypeChecker
            seus.set_density(
                mass_qty=None,
                vol_qty=None,
                mass_unit='g',
                vol_unit='ml'
            )

    def test_raises_exception_if_either_qty_is_zero(self):
        """Check that we can't pass zero as a parameter to either of the qty values."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we pass in zero to either;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.set_density(
                mass_qty=0,
                vol_qty=12,
                mass_unit='g',
                vol_unit='ml'
            )
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.set_density(
                mass_qty=12,
                vol_qty=0,
                mass_unit='g',
                vol_unit='ml'
            )

    def test_raises_exception_if_unit_not_recognised(self):
        """Checks we get an exception if one of the units are invalid."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if either argument has an unknown unit;
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            seus.set_density(
                mass_qty=10,
                vol_qty=12,
                mass_unit='fake',
                vol_unit='ml'
            )
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            seus.set_density(
                mass_qty=10,
                vol_qty=12,
                mass_unit='f',
                vol_unit='fake'
            )

    def test_raises_exception_if_unit_is_incorrect_type(self):
        """Checks we get an exception if one of the units are of an incorrect type."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if either argument has an incorrect unit type;
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            seus.set_density(
                mass_qty=10,
                vol_qty=12,
                mass_unit='ml',
                vol_unit='ml'
            )
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            seus.set_density(
                mass_qty=10,
                vol_qty=12,
                mass_unit='g',
                vol_unit='g'
            )


class TestUnsetDensity(TestCase):
    """Tests for the unset_density method."""

    def test_unset_density_unsets_density(self):
        """Checks the method does actually unset the density."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data(g_per_ml=1.2))

        # Check the density started out as defined;
        self.assertTrue(seus.density_is_defined)

        # Now unset it;
        seus.unset_density()

        # Now check it is no longer defined;
        self.assertFalse(seus.density_is_defined)


class TestSetPieceMass(TestCase):
    """Tests for the set_piece_mass method."""

    def test_sets_piece_mass_correctly(self):
        """Check the density can be set with arbitrary units correctly."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check the density is not configured;
        self.assertFalse(seus.piece_mass_is_defined)

        # Set the density;
        seus.set_piece_mass(
            mass_qty=1.5,
            mass_unit='kg',
            num_pieces=2
        )

        # Assert the density was set correctly;
        self.assertEqual(750, seus.piece_mass_g)

    def test_raises_exception_if_value_is_none(self):
        """Check that we can't pass None values into this method. We
        should be using the unset_piece_mass method to unset the instance's density."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we pass in None to both;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            # noinspection PyTypeChecker
            seus.set_piece_mass(
                mass_qty=None,
                mass_unit='g',
                num_pieces=2
            )

    def test_raises_exception_if_either_qty_is_zero(self):
        """Check that we can't pass zero as a parameter to either of the qty values."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we pass in zero to either;
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.set_piece_mass(
                mass_qty=0,
                mass_unit='g',
                num_pieces=2
            )
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.set_piece_mass(
                mass_qty=100,
                mass_unit='g',
                num_pieces=0
            )

    def test_raises_exception_if_unit_not_recognised(self):
        """Checks we get an exception if one of the units are invalid."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if either argument has an unknown unit;
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            seus.set_piece_mass(
                mass_qty=100,
                mass_unit='fake',
                num_pieces=1
            )

    def test_raises_exception_if_unit_is_incorrect_type(self):
        """Checks we get an exception if the mass unit is not a mass unit."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if either argument has an incorrect unit type;
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            seus.set_piece_mass(
                mass_qty=100,
                mass_unit='ml',
                num_pieces=2
            )
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            seus.set_piece_mass(
                mass_qty=100,
                mass_unit='pc',
                num_pieces=2
            )


class TestUnsetPieceMass(TestCase):
    """Tests for the unset_peice_mass method."""

    def test_unset_density_unsets_piece_mass(self):
        """Checks the method does actually unset the piece mass."""
        # Create the test instance;
        seus = model.quantity.HasSettableExtendedUnits(fx.get_extended_units_data(piece_mass_g=100))

        # Check the piece mass started out as defined;
        self.assertTrue(seus.piece_mass_is_defined)

        # Now unset it;
        seus.unset_piece_mass()

        # Now check it is no longer defined;
        self.assertFalse(seus.piece_mass_is_defined)


class TestLoadData(TestCase):
    """Tests for the load data method."""

    def test_data_loaded_correctly(self):
        """Checks that data is loaded in correctly."""
        # Create a test instance without data;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check the persistable data is empty;
        self.assertEqual(
            {
                'g_per_ml': None,
                'piece_mass_g': None
            },
            seus.persistable_data['extended_units_data']
        )

        # Load some data;
        data = {'extended_units_data': fx.get_extended_units_data(g_per_ml=1.2, piece_mass_g=100)}
        seus.load_data(data)

        # Check the persistable data is now populated;
        self.assertEqual(
            {
                'g_per_ml': 1.2,
                'piece_mass_g': 100
            },
            seus.persistable_data['extended_units_data']
        )

    def test_raises_exception_if_field_missing_from_data(self):
        """Checks that data is loaded in correctly."""
        # Create a test instance without data;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we try to load data with a field missing;
        with self.assertRaises(KeyError):
            seus.load_data({'extended_units_data': {}})

    # noinspection PyTypeChecker
    def test_raises_exception_if_try_to_load_invalid_data(self):
        """Checks that we get an exception if we try to load invalid data;"""
        # Create a test instance without data;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get an exception if we try to load invalid data;
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.load_data({'extended_units_data': fx.get_extended_units_data(
                g_per_ml="fake",
                piece_mass_g=100
            )})
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.load_data({'extended_units_data': fx.get_extended_units_data(
                g_per_ml=1.2,
                piece_mass_g="fake"
            )})
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            seus.load_data({'extended_units_data': fx.get_extended_units_data(
                g_per_ml=-1,
                piece_mass_g=100
            )})
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            seus.load_data({'extended_units_data': fx.get_extended_units_data(
                g_per_ml=1.2,
                piece_mass_g=0
            )})

    def test_no_error_if_dict_has_no_extended_units_key(self):
        """Check that we don't get an exception if the dict has not extended units key."""
        # Create a test instance;
        seus = model.quantity.HasSettableExtendedUnits()

        # Check we get no error if we load an empty dict;
        seus.load_data({})
