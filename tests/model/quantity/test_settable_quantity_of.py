"""Tests for SettableQuantityOf class.
"""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):
    def test_get_correct_instance(self):
        self.assertTrue(isinstance(model.quantity.HasSettableQuantityOf(
            qty_subject=mock.Mock()
        ), model.quantity.HasSettableQuantityOf))

    def test_loads_data_if_provided(self):
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=mock.Mock(),
            quantity_data=model.quantity.QuantityData(quantity_in_g=150, pref_unit='kg')
        )


class TestResetPrefUnit(TestCase):
    def test_pref_unit_is_reset_correctly(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        sqo._quantity_data['pref_unit'] = 'L'
        self.assertEqual(sqo._quantity_data['pref_unit'], 'L')
        sqo._reset_qty_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'g')


class TestSanitisePrefUnit(TestCase):
    def test_valid_vol_unit_is_not_changed(self):
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=fx.HasReadableExtendedUnitsTestable(g_per_ml=1.2),
        )
        sqo._quantity_data['pref_unit'] = 'l'
        sqo._sanitise_qty_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'l')

    def test_unknown_unit_is_reset(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        sqo._quantity_data['pref_unit'] = 'fake'
        sqo._sanitise_qty_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'g')

    def test_unconfigured_pc_unit_is_reset(self):
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=fx.HasReadableExtendedUnitsTestable(piece_mass_g=None),
        )
        sqo._quantity_data['pref_unit'] = 'pc'
        sqo._sanitise_qty_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'g')


class TestSetQuantity(TestCase):
    # Test the setter functionality;
    def test_sets_value_correctly(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        sqo.set_quantity(1.2, 'kg')
        self.assertEqual(sqo._quantity_data['quantity_in_g'], 1200)

    def test_raises_exception_if_quantity_invalid(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            sqo.set_quantity(-4, 'kg')
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            sqo.set_quantity('invalid', 'kg')  # noqa

    def test_raises_exception_if_unit_not_recognised(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            sqo.set_quantity(4, 'fake')

    def test_raises_exception_if_extended_units_used_but_not_supported(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            sqo.set_quantity(4, 'L')

    def test_raises_exception_if_vol_unit_used_but_not_configured(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=fx.HasReadableExtendedUnitsTestable(g_per_ml=None))
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            sqo.set_quantity(4, 'L')

    def test_raises_exception_if_piece_unit_used_but_not_configured(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=fx.HasReadableExtendedUnitsTestable(piece_mass_g=None))
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            sqo.set_quantity(4, 'pc')


class TestUnsetQuantity(TestCase):
    def test_quantity_unset_correctly(self):
        sqo = model.quantity.HasSettableQuantityOf(qty_subject=mock.Mock())
        sqo._quantity_data['quantity_in_g'] = 120
        sqo.unset_quantity()
        self.assertIsNone(sqo._quantity_data['quantity_in_g'])


class TestLoadData(TestCase):
    """Tests the load_data method on SettableQuantityOf."""
    def test_loads_data_with_mass_pref_unit_correctly_when_subject_has_no_extended_units(self):
        """Check that we can load data correctly if the pref unit in the data is a mass, and
        the subject does not support extended units."""
        # Create a test instance, with a mass as a pref unit;
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=mock.Mock(),
        )

        # Try and load the data;
        sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='kg'))

        # Check that the data is set correctly;
        self.assertEqual(150, sqo.quantity_in_g)
        self.assertTrue('kg', sqo.qty_pref_unit)

    def test_loads_data_with_vol_pref_unit_correctly(self):
        """Check that we can load data correctly if the pref unit is a volume, and density is configured
        on the subject."""
        # Create a test instance, with a subject with density configured;
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=fx.HasReadableExtendedUnitsTestable(g_per_ml=2)
        )

        # Load the data in;
        sqo.load_data(model.quantity.QuantityData(quantity_in_g=60, pref_unit='ml'))

        # Check the data is what it should be;
        self.assertEqual(60, sqo.quantity_in_g)
        self.assertEqual('ml', sqo.qty_pref_unit)

    def test_raises_exception_if_pref_unit_extended_and_extended_not_available(self):
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=mock.Mock(),
        )
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='L'))

    def test_raises_exception_if_pref_unit_vol_but_not_configured(self):
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=fx.HasReadableExtendedUnitsTestable(),
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='l'))

    def test_raises_exception_if_pref_unit_pc_but_not_configured(self):
        sqo = model.quantity.HasSettableQuantityOf(
            qty_subject=fx.HasReadableExtendedUnitsTestable(),
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='pc'))
