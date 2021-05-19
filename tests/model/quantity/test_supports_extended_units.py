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


class TestPieceMassG(TestCase):
    """Tests general functionality of peice_mass_g property."""

    def test_returns_correct_value_if_defined(self):
        """Checks we get the correct value back out, if defined."""
        # Create a testable instance;
        seu = fx.SupportsExtendedUnitsTestable(piece_mass_g=150)

        # Check the correct value is returned;
        self.assertEqual(150, seu.piece_mass_g)

    def test_raises_exception_if_not_defined(self):
        """Checks we get an exception if not defined."""
        # Create a testable instance, with no mass set;
        seu = fx.SupportsExtendedUnitsTestable(piece_mass_g=None)

        # Assert we get an error if we try and call the property;
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            _ = seu.piece_mass_g


class TestDensityIsDefined(TestCase):
    """Tests general functionality for density_is_defined property."""

    def test_returns_true_if_density_is_defined(self):
        """Checks the property returns True if the density is defined."""
        # Create a test instance with density defined;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.2)

        # Check the property returns True;
        self.assertTrue(seu.density_is_defined)

    def test_returns_false_if_density_not_defined(self):
        """Checks the property returns False if the density is not defined."""
        # Create a test instance with the density undefined;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=None)

        # Check the property returns False;
        self.assertFalse(seu.density_is_defined)


class TestPieceMassIsDefined(TestCase):
    """Tests general functionality for piece_mass_is_defined property."""

    def test_returns_true_if_piece_mass_is_defined(self):
        """Checks the property returns True if the piece mass is defined."""
        # Create a test instance with the piece mass defined;
        seu = fx.SupportsExtendedUnitsTestable(piece_mass_g=150)

        # Assert the property returns True;
        self.assertTrue(seu.piece_mass_is_defined)

    def test_returns_false_if_piece_mass_not_defined(self):
        """Checks the property returns False if the piece mass is not defined."""
        # Create a test instance with the peice mass undefined;
        seu = fx.SupportsExtendedUnitsTestable(piece_mass_g=None)

        # Check the method returns False;
        self.assertFalse(seu.piece_mass_is_defined)


class TestAvailableUnits(TestCase):
    """Tests the general functionality of the available units method."""

    def test_returns_only_mass_units_if_no_units_available(self):
        # Create an instance with no extended units configuired;
        seu = fx.SupportsExtendedUnitsTestable()

        # Check the units returned match those on the global mass units list;
        self.assertEqual(set(model.quantity.MASS_UNITS), set(seu.available_units))

    def test_includes_volume_units_if_volume_units_configured(self):
        """Checks that we get mass and volume units if density is configured."""
        # Create an instance with volume configured;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.2)

        # Check we get volume units on the list;
        self.assertEqual(set(
            model.quantity.MASS_UNITS + model.quantity.VOL_UNITS
        ), set(seu.available_units))

    def test_includes_pc_mass_units_if_piece_mass_units_configured(self):
        """Checks that we get peice mass units if the piece mass is configured."""
        # Create an instance with piece mass configured;
        seu = fx.SupportsExtendedUnitsTestable(piece_mass_g=1.2)

        # Check we get piece units on the list;
        self.assertEqual(set(
            model.quantity.MASS_UNITS + model.quantity.PC_UNITS
        ), set(seu.available_units))

    def test_includes_all_units_if_all_units_configured(self):
        """Checks we get all units if all units are configured."""
        # Create an instance with all extended units configured;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.1, piece_mass_g=1.2)

        # Check we get piece units on the list;
        self.assertEqual(set(model.quantity.QTY_UNITS), set(seu.available_units))


class TestUnitsAreConfigured(TestCase):
    """Tests the general functionality of the units_are_congigured method."""

    def test_returns_true_if_unit_is_mass(self):
        """Checks that we get True if unit is mass, even if no extended units
        are configured."""
        # Create an instance with no extended units;
        seu = fx.SupportsExtendedUnitsTestable()

        # Check mass units are configured;
        self.assertTrue(seu.units_are_configured(*model.quantity.MASS_UNITS))

    def test_returns_false_if_unit_is_vol_and_density_not_configured(self):
        """Checks that we get False if unit is volume and density is not configured."""
        # Create an instance with no density unit;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=None)

        # Check each volumetric unit is not available;
        for vol_unit in model.quantity.VOL_UNITS:
            self.assertFalse(seu.units_are_configured(vol_unit))

    def test_returns_true_if_unit_is_vol_and_density_is_configured(self):
        """Checks that we get True if unit is volume and density is configured."""
        # Create an instance with density configured;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.2)

        # Check each volumetric unit is available;
        for vol_unit in model.quantity.VOL_UNITS:
            self.assertTrue(seu.units_are_configured(vol_unit))

    def test_returns_true_for_both_peice_and_vol_if_both_configured(self):
        """Check that we get True if we query a list with both piece and volume,
        and both are configured."""
        # Create an instance with both piece and volume configured;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.2, piece_mass_g=150)

        # Check we get True if we query a mixed list;
        self.assertTrue(seu.units_are_configured("pc", "L", "kg"))

    def test_raises_exception_if_unit_not_recognised(self):
        """Test to make sure we get an exception if the unit isn't recognised."""
        # Create an instance;
        seu = fx.SupportsExtendedUnitsTestable()

        # Assert we get an exception if the unit isnt recognised;
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            seu.units_are_configured("fake")


class TestPersistableData(TestCase):
    """Tests the general functionality of the persistable data property."""

    def test_data_dict_updated_correctly_when_no_extended_units(self):
        """Checks that the dict is updated correctly when there are no extended units
        on the instance."""
        # Create an instance with no exteded units;
        seu = fx.SupportsExtendedUnitsTestable()

        # Check the dict has the heading, with no data;
        data = {"extended_units_data": model.quantity.ExtendedUnitsData(
            g_per_ml=None,
            piece_mass_g=None
        )}
        self.assertEqual(data, seu.persistable_data)

    def test_data_dict_updated_correctly_when_extended_units_configured(self):
        """Checks that the dict is updated correctly when there are extended units
        on the instance."""
        # Create an instance with extended units configured;
        seu = fx.SupportsExtendedUnitsTestable(g_per_ml=1.2, piece_mass_g=150)

        # Check the dict has the heading, with no data;
        data = {"extended_units_data": model.quantity.ExtendedUnitsData(
            g_per_ml=1.2,
            piece_mass_g=150
        )}
        self.assertEqual(data, seu.persistable_data)
