"""Tests for BaseQuantityOf class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as fx


class TestSubject(TestCase):
    """Tests for the subject property."""

    def test_subject_returned_correctly(self):
        """Check we get the same subject back as we put in."""
        # Create a mock subject to send in;
        s = mock.Mock()

        # Create the test instance, passing the subject in;
        bqo = fx.BaseQuantityOfTestable(
            subject=s,
            quantity_data=fx.get_qty_data()
        )

        # Check we get the same subject back out;
        self.assertTrue(s is bqo.subject)


class TestQuantityInG(TestCase):
    """Tests for the quantity_in_g property."""

    def test_returns_qty_in_g_if_set(self):
        """Check the quantity in grams is returned correctly if set."""
        # Create a test instance with a quantity in grams value set;
        bqo = fx.BaseQuantityOfTestable(subject=mock.Mock(), quantity_data=fx.get_qty_data(qty_in_g=22))

        # Check that we get the same value for the qty in grams back out;
        self.assertEqual(22, bqo.quantity_in_g)

    def test_raises_exception_if_not_set(self):
        """Check we get an exception if the quantity in grams is not set."""
        # Create a test instance with no value for quantity in grams;
        bqo = fx.BaseQuantityOfTestable(subject=mock.Mock(), quantity_data=fx.get_qty_data())

        # Now check we get an exception if we try and access the qty in grams property;
        with self.assertRaises(model.quantity.exceptions.UndefinedQuantityError):
            _ = bqo.quantity_in_g


class TestPrefUnit(TestCase):
    """Tests the pref_unit property."""

    def test_pref_mass_unit_returned_correctly_if_ext_units_unsupported(self):
        """Checks the pref unit is returned correctly if the unit is a mass, and the subject
        does not support extended units."""
        # Create a test instance with the pref unit set as kg.
        bqo = fx.BaseQuantityOfTestable(subject=mock.Mock(), quantity_data=fx.get_qty_data(
            pref_unit='kg'
        ))

        # Check we get kg back out;
        self.assertEqual("kg", bqo.pref_unit)

    def test_pref_vol_unit_returned_correctly_if_dens_configured(self):
        """Checks we get a volume pref qty back, if one is set and the subject has density configured."""
        # Create a test instance with a volume pref unit and density configured;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(g_per_ml=1.2),
            quantity_data=fx.get_qty_data(
                pref_unit='l'
            )
        )

        # Check we can get the volumetric unit back out;
        self.assertEqual("l", bqo.pref_unit)

    def test_pref_pc_unit_returned_correctly_if_pc_mass_configured(self):
        """Checks we get a pc mass pref qty back, if one is set and the subject has pc mass configured."""
        # Create a test instance with a pc mass pref unit and piece mass configured;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(piece_mass_g=120),
            quantity_data=fx.get_qty_data(
                pref_unit='pc'
            )
        )

        # Check we can get the volumetric unit back out;
        self.assertEqual("pc", bqo.pref_unit)

    def test_pref_unit_case_corrected(self):
        """Checks the case will be corrected if the pref unit is supplied in incorrect case."""
        # Create a test instance with a unit specified with incorrect case;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(g_per_ml=1.2),
            quantity_data=fx.get_qty_data(
                pref_unit='L'
            )
        )

        # Check we can get the unit back out, with the case corrected;
        self.assertEqual("l", bqo.pref_unit)

    def test_exception_if_unit_not_recognised(self):
        """Checks we get an exception if we try and access a pref unit which is not recognised."""
        # Create a test instance with a unit specified with an unrecognised unit;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data(
                pref_unit='fake'
            )
        )

        # Check we get an exception if we try to access it;
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            _ = bqo.pref_unit

    def test_exception_if_extended_units_used_and_subject_does_not_support_them(self):
        """Checks we get an exception if an extended unit is used with a subject that does not support it."""
        # Create a test instance with an extended unit, and a subject that doesn't support ext units;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data(
                pref_unit='l'
            )
        )

        # Check we get an exception if we try to access it;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            _ = bqo.pref_unit

    def test_exception_if_pref_unit_volume_and_density_not_configured_on_subject(self):
        """Checks we get an exception if pref unit is a volume, and the subject supports extended units
        but does not have density configured."""
        # Create a test instance with a subject which supports extended units, but does not have dens configured;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(),
            quantity_data=fx.get_qty_data(
                pref_unit='L'
            )
        )

        # Check we get an exception when we access the property;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = bqo.pref_unit

    def test_exception_if_pref_unit_pc_and_piece_mass_not_configured_on_subject(self):
        """Checks we get an exception if pref unit is a pc mass, and the subject supports extended units
        but does not have piece mass configured."""
        # Create a test instance with a subject which supports extended units, but does not have piece mass configured;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(),
            quantity_data=fx.get_qty_data(
                pref_unit='pc'
            )
        )

        # Check we get an exception when we access the property;
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            _ = bqo.pref_unit


class TestRefQty(TestCase):
    """Tests for the ref_qty property."""

    def test_returns_ref_mass_qty_correctly(self):
        """Test we get the correct value if pref unit is a mass."""
        # Create a test instance with qty defined and pref unit as mass unit.
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data(qty_in_g=120, pref_unit='kg')
        )

        # Check we get the right ref qty back out;
        self.assertEqual(0.12, bqo.ref_qty)

    def test_returns_ref_vol_qty_correctly(self):
        """Test we get the correct value if the pref unit is a volume."""
        # Create a test instance with qty defined as a volume;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(g_per_ml=1.2),
            quantity_data=fx.get_qty_data(qty_in_g=60, pref_unit="L")
        )

        # Check we get the right value back;
        self.assertEqual(0.05, bqo.ref_qty)

    def test_returns_ref_pc_mass_correctly(self):
        """Test we get the correct value if the pref unit is a pc mass."""
        # Create a test instance wity qty defined as a pc mass;
        qo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(piece_mass_g=150),
            quantity_data=fx.get_qty_data(qty_in_g=300, pref_unit="pc")
        )

        # Check we get the right value back;
        self.assertEqual(qo.ref_qty, 2)

    def test_raises_exception_if_pref_unit_is_volume_and_density_not_defined(self):
        """Check that we get an exception if we ask for the ref quantity and the unit
        is not defined on the instance."""

        # Create a test instance which does not define density;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(),
            quantity_data=fx.get_qty_data(qty_in_g=120, pref_unit="L")
        )

        # Check that we get an exception when we ask for the ref quantity;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = bqo.ref_qty

    def test_raises_exception_if_extended_units_not_supported_and_unit_is_volume(self):
        """Check that we get an excpetion if the pref unit is a volume and extended units are not supported."""
        # Create a test instance with a volume unit, and a subject that does not support extended units;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data(qty_in_g=120, pref_unit="L")
        )

        # Check the exception is raised;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            _ = bqo.ref_qty


class TestIsDefined(TestCase):
    """Tests for the is_defined property."""

    def test_returns_true_if_quantity_in_g_defined(self):
        """Check the property returns True if the quantity_in_g is defined."""
        # Create a test instance with the quantity fully defined;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data(qty_in_g=120)
        )

        # Check we get True from the method;
        self.assertTrue(bqo.quantity_is_defined)

    def test_returns_false_if_quantity_in_g_not_defined(self):
        """Check the property returns False if the quantity_in_g is not defined."""
        # Create a test instance with the quantity fully not defined;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data()
        )

        # Check we get True from the method;
        self.assertFalse(bqo.quantity_is_defined)


class TestPersistableData(TestCase):
    """Tests for the persistable_data property."""

    def test_returns_persistable_data_correctly(self):
        """Check we get the correct values back."""
        # Create some test data;
        data = fx.get_qty_data(qty_in_g=120, pref_unit='kg')

        # Create a test instance, passing the data in;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=data
        )

        # Check the data we get back is correct;
        self.assertEqual(data, bqo.persistable_data)

    def test_raises_exception_if_subject_pref_unit_is_not_configured(self):
        """Check we get an exception if the pref unit is an extended unit, and the subject, doesn't
        have it configured."""
        # Create a test instance with extended units supported but not configured;
        bqo = fx.BaseQuantityOfTestable(
            subject=fx.SupportsExtendedUnitsTestable(),
            quantity_data=fx.get_qty_data(qty_in_g=1.2, pref_unit='L')
        )

        # Check we get the right exception when we try to access the persistable data;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = bqo.persistable_data

    def test_raises_exception_if_subject_pref_unit_is_not_supported(self):
        """Check we get an exception if the pref unit is an extended unit, and the subject, doesn't
        support extended units."""
        # Create a test instance with a subject that does not support extended units;
        bqo = fx.BaseQuantityOfTestable(
            subject=mock.Mock(),
            quantity_data=fx.get_qty_data(qty_in_g=1.2, pref_unit='L')
        )

        # Check we get the right exception when we try to access the persistable data;
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            _ = bqo.persistable_data
