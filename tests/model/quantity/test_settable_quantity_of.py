from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):
    def test_get_correct_instance(self):
        self.assertTrue(isinstance(model.quantity.SettableQuantityOf(
            subject=mock.Mock()
        ), model.quantity.SettableQuantityOf))

    def test_loads_data_if_provided(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=mock.Mock(),
            quantity_data=model.quantity.QuantityData(quantity_in_g=150, pref_unit='kg')
        )


class TestResetPrefUnit(TestCase):
    def test_pref_unit_is_reset_correctly(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        sqo._quantity_data['pref_unit'] = 'L'
        self.assertEqual(sqo._quantity_data['pref_unit'], 'L')
        sqo._reset_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'g')


class TestSanitisePrefUnit(TestCase):
    def test_valid_vol_unit_is_not_changed(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=fx.get_subject_with_density(g_per_ml=1.2),
        )
        sqo._quantity_data['pref_unit'] = 'l'
        sqo._sanitise_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'l')

    def test_unknown_unit_is_reset(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        sqo._quantity_data['pref_unit'] = 'fake'
        sqo._sanitise_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'g')

    def test_unconfigured_pc_unit_is_reset(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=fx.get_subject_with_pc_mass(piece_mass_g=None),
        )
        sqo._quantity_data['pref_unit'] = 'pc'
        sqo._sanitise_pref_unit()
        self.assertEqual(sqo._quantity_data['pref_unit'], 'g')


class TestSetQuantity(TestCase):
    # Test the setter functionality;
    def test_sets_value_correctly(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        sqo.set_quantity(1.2, 'kg')
        self.assertEqual(sqo._quantity_data['quantity_in_g'], 1200)

    def test_raises_exception_if_quantity_invalid(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            sqo.set_quantity(-4, 'kg')
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            sqo.set_quantity('invalid', 'kg')  # noqa

    def test_raises_exception_if_unit_not_recognised(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            sqo.set_quantity(4, 'fake')

    def test_raises_exception_if_extended_units_used_but_not_supported(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            sqo.set_quantity(4, 'L')

    def test_raises_exception_if_vol_unit_used_but_not_configured(self):
        sqo = model.quantity.SettableQuantityOf(subject=fx.get_subject_with_density(g_per_ml=None))
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            sqo.set_quantity(4, 'L')

    def test_raises_exception_if_piece_unit_used_but_not_configured(self):
        sqo = model.quantity.SettableQuantityOf(subject=fx.get_subject_with_pc_mass(piece_mass_g=None))
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            sqo.set_quantity(4, 'pc')


class TestUnsetQuantity(TestCase):
    def test_quantity_unset_correctly(self):
        sqo = model.quantity.SettableQuantityOf(subject=mock.Mock())
        sqo._quantity_data['quantity_in_g'] = 120
        sqo.unset_quantity()
        self.assertIsNone(sqo._quantity_data['quantity_in_g'])


class TestLoadData(TestCase):
    def test_loads_data_with_mass_pref_unit_correctly(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=mock.Mock(),
        )
        sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='kg'))
        self.assertTrue(sqo.quantity_in_g == 150)
        self.assertTrue(sqo.pref_unit == 'kg')

    def test_loads_data_with_vol_pref_unit_correctly(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=fx.get_subject_with_density(g_per_ml=2)
        )
        sqo.load_data(model.quantity.QuantityData(quantity_in_g=60, pref_unit='ml'))
        self.assertTrue(sqo.quantity_in_g == 60)
        self.assertTrue(sqo.pref_unit == 'ml')

    def test_raises_exception_if_pref_unit_extended_and_extended_not_available(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=mock.Mock(),
        )
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='L'))

    def test_raises_exception_if_pref_unit_vol_but_not_configured(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=fx.get_subject_with_density(),
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='l'))

    def test_raises_exception_if_pref_unit_pc_but_not_configured(self):
        sqo = model.quantity.SettableQuantityOf(
            subject=fx.get_subject_with_pc_mass(),
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            sqo.load_data(model.quantity.QuantityData(quantity_in_g=150, pref_unit='pc'))
