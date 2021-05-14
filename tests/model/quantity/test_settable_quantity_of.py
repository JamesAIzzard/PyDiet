from unittest import TestCase

import model
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):
    def test_get_correct_instance(self):
        self.assertTrue(isinstance(fx.get_undefined_has_settable_quantity(), model.quantity.SettableQuantityOf))


class TestQuantityInG(TestCase):
    # Test the setter functionality;
    def test_sets_value_correctly(self):
        hq = fx.get_undefined_has_settable_quantity()
        hq.quantity_in_g = 150
        self.assertTrue(hq.quantity_in_g == 150)
        self.assertTrue(hq._quantity_in_g == 150)

    def test_unsets_value_correctly(self):
        hq = fx.get_undefined_has_settable_quantity()
        hq.quantity_in_g = None
        self.assertTrue(hq._quantity_in_g == None)  # noqa

    def test_raises_exception_if_quantity_invalid(self):
        hq = fx.get_undefined_has_settable_quantity()
        with self.assertRaises(model.quantity.exceptions.InvalidQtyError):
            hq.quantity_in_g = "none"


class TestQuantityPrefUnit(TestCase):
    # Again, testing the setter;
    def test_sets_value_correctly(self):
        hq = fx.get_undefined_has_settable_quantity()
        hq.quantity_pref_unit = 'kg'
        self.assertTrue(hq.quantity_pref_unit == 'kg')
        self.assertTrue(hq._quantity_pref_unit == 'kg')

    def test_raises_exception_if_unit_unrecognised(self):
        hq = fx.get_undefined_has_settable_quantity()
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            hq.quantity_pref_unit = 'madeups'

    def test_raises_exception_if_unit_not_configured(self):
        hq = fx.get_undefined_has_settable_quantity()
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            hq.quantity_pref_unit = 'L'
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            hq.quantity_pref_unit = 'pc'

    def test_sets_volume_unit_if_density_configured(self):
        hq = model.quantity.HasSettableQuantityOf(
            subject=fx.get_has_bulk_with_09_density(),
        )
        hq.quantity_pref_unit = 'l'
        self.assertTrue(hq.quantity_pref_unit == 'l')

    def test_sets_pc_unit_if_pc_mass_configured(self):
        hq = model.quantity.HasSettableQuantityOf(
            subject=fx.get_has_bulk_with_30_pc_mass(),
        )
        hq.quantity_pref_unit = 'pc'
        self.assertTrue(hq.quantity_pref_unit == 'pc')


class TestSetQuantity(TestCase):
    def test_sets_quantity_correctly(self):
        # Try with a mass;
        hq = model.quantity.HasSettableQuantityOf(subject=model.quantity.HasBulk())
        hq.set(
            qty=1.5,
            unit='kg'
        )
        self.assertTrue(hq.quantity_in_g == 1500)

        # Try with a volume;
        hq = model.quantity.HasSettableQuantityOf(subject=fx.get_has_bulk_with_09_density())
        hq.set(
            qty=1.5,
            unit='L'
        )
        self.assertTrue(hq.quantity_in_g == 1350)

        # Try with piece mass;
        hq = model.quantity.HasSettableQuantityOf(subject=fx.get_has_bulk_with_30_pc_mass())
        hq.set(
            qty=1.5,
            unit='pc'
        )
        self.assertTrue(hq.quantity_in_g == 45)

    def test_raises_exception_if_density_not_configured(self):
        hq = model.quantity.HasSettableQuantityOf(subject=model.quantity.HasBulk())
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            hq.set(
                qty=1.5,
                unit='L'
            )

    def test_raises_exception_if_piece_mass_not_configured(self):
        hq = model.quantity.HasSettableQuantityOf(subject=model.quantity.HasBulk())
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            hq.set(
                qty=1.5,
                unit='pc'
            )


class TestLoadData(TestCase):
    def test_loads_data_correctly(self):
        hq = model.quantity.HasSettableQuantityOf(
            subject=model.quantity.HasBulk(),
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=150,
                quantity_pref_unit='kg'
            )
        )
        self.assertTrue(hq.quantity_in_g == 150)
        self.assertTrue(hq.quantity_pref_unit == 'kg')

    def test_falls_back_to_g_if_qty_pref_unit_not_configured(self):
        # First, try with a density unit which isn't configured;
        hq = model.quantity.HasSettableQuantityOf(
            subject=model.quantity.HasBulk(),
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=120,
                quantity_pref_unit='L'
            )
        )
        self.assertTrue(hq.quantity_in_g == 120)
        self.assertTrue(hq.quantity_pref_unit == 'g')

        # Now try with a peice mass unit;
        hq = model.quantity.HasSettableQuantityOf(
            subject=model.quantity.HasBulk(),
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=120,
                quantity_pref_unit='pc'
            )
        )
        self.assertTrue(hq.quantity_in_g == 120)
        self.assertTrue(hq.quantity_pref_unit == 'g')


class TestPersistableData(TestCase):
    def test_returns_correct_data(self):
        hq = model.quantity.HasSettableQuantityOf(
            subject=model.quantity.HasBulk(),
            quantity_data=model.quantity.QuantityData(
                quantity_in_g=120,
                quantity_pref_unit='kg'
            )
        )
        self.assertEqual(hq.persistable_data, model.quantity.QuantityData(
            quantity_in_g=120,
            quantity_pref_unit='kg'
        ))
