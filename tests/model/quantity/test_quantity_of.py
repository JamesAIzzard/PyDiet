from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as fx


class TestConstructor(TestCase):

    def test_correct_instance_returned(self):
        self.assertTrue(isinstance(model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src()
        ), model.quantity.QuantityOf))


class TestSubject(TestCase):
    def test_subject_returned_correctly(self):
        s = mock.Mock()
        qo = model.quantity.QuantityOf(subject=s, quantity_data_src=fx.get_qty_data_src())
        self.assertTrue(s is qo._subject)


class TestQuantityInG(TestCase):
    def test_returns_qty_in_g_if_set(self):
        qo = model.quantity.QuantityOf(subject=mock.Mock(), quantity_data_src=fx.get_qty_data_src(
            qty_in_g=5))
        self.assertTrue(qo.quantity_in_g == 5)

    def test_raises_exception_if_not_set(self):
        qo = model.quantity.QuantityOf(subject=mock.Mock(), quantity_data_src=fx.get_qty_data_src())
        with self.assertRaises(model.quantity.exceptions.UndefinedQuantityError):
            _ = qo.quantity_in_g


class TestPrefUnit(TestCase):
    def test_pref_mass_unit_returned_correctly(self):
        qo = model.quantity.QuantityOf(subject=mock.Mock(), quantity_data_src=fx.get_qty_data_src(
            pref_unit='kg'
        ))
        self.assertTrue(qo.pref_unit == 'kg')

    def test_pref_vol_unit_returned_correctly(self):
        qo = model.quantity.QuantityOf(subject=fx.SupportsExtendedUnitsTestable(
            g_per_ml=1.2
        ), quantity_data_src=fx.get_qty_data_src(
            pref_unit='l'
        ))
        self.assertTrue(qo.pref_unit == 'l')

    def test_pref_pc_unit_returned_correctly(self):
        qo = model.quantity.QuantityOf(subject=fx.SupportsExtendedUnitsTestable(
            piece_mass_g=100
        ), quantity_data_src=fx.get_qty_data_src(
            pref_unit='kg'
        ))
        self.assertTrue(qo.pref_unit == 'kg')

    def test_pref_unit_case_corrected(self):
        qo = model.quantity.QuantityOf(subject=fx.SupportsExtendedUnitsTestable(
            g_per_ml=1.2
        ), quantity_data_src=fx.get_qty_data_src(
            pref_unit='L'
        ))
        self.assertTrue(qo.pref_unit == 'l')

    def test_exception_if_unit_not_recognised(self):
        qo = model.quantity.QuantityOf(subject=fx.SupportsExtendedUnitsTestable(
            g_per_ml=1.2
        ), quantity_data_src=fx.get_qty_data_src(
            pref_unit='fake'
        ))
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            _ = qo.pref_unit

    def test_exception_if_extended_units_used_and_subject_does_not_support_them(self):
        qo = model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src(pref_unit='l')
        )
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            _ = qo.pref_unit

    def test_exception_if_pref_unit_volume_and_density_not_configured_on_subject(self):
        qo = model.quantity.QuantityOf(
            subject=fx.SupportsExtendedUnitsTestable(g_per_ml=None),
            quantity_data_src=fx.get_qty_data_src(pref_unit='L')
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = qo.pref_unit

    def test_exception_if_pref_unit_pc_and_piece_mass_not_configured_on_subject(self):
        qo = model.quantity.QuantityOf(
            subject=fx.SupportsExtendedUnitsTestable(piece_mass_g=None),
            quantity_data_src=fx.get_qty_data_src(pref_unit='pc')
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            _ = qo.pref_unit


class TestRefQty(TestCase):
    def test_returns_ref_mass_qty_correctly(self):
        qo = model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=120, pref_unit='kg')
        )
        self.assertEqual(qo.ref_qty, 0.12)

    def test_returns_ref_vol_qty_correctly(self):
        qo = model.quantity.QuantityOf(
            subject=fx.SupportsExtendedUnitsTestable(g_per_ml=1.2),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=60, pref_unit="L")
        )
        self.assertEqual(qo.ref_qty, 0.05)

    def test_returns_ref_pc_mass_correctly(self):
        qo = model.quantity.QuantityOf(
            subject=fx.SupportsExtendedUnitsTestable(piece_mass_g=150),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=300, pref_unit="pc")
        )
        self.assertEqual(qo.ref_qty, 2)

    def test_raises_exception_if_pref_unit_is_volume_and_density_not_defined(self):
        qo = model.quantity.QuantityOf(
            subject=fx.SupportsExtendedUnitsTestable(),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=120, pref_unit="L")
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = qo.ref_qty

    def test_raises_exception_if_extended_units_not_supported_and_unit_is_volume(self):
        qo = model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=120, pref_unit="L")
        )
        with self.assertRaises(model.quantity.exceptions.UnsupportedExtendedUnitsError):
            _ = qo.ref_qty


class TestIsDefined(TestCase):
    def test_returns_true_if_quantity_in_g_defined(self):
        qo = model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=120)
        )
        self.assertTrue(qo.is_defined)

    def test_returns_false_if_quantity_in_g_defined(self):
        qo = model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src()
        )
        self.assertFalse(qo.is_defined)


class TestPersistableData(TestCase):
    def test_returns_persistable_data_correctly(self):
        qo = model.quantity.QuantityOf(
            subject=mock.Mock(),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=120, pref_unit='kg')
        )
        self.assertEqual(qo.persistable_data, model.quantity.QuantityData(
            quantity_in_g=120,
            pref_unit='kg'
        ))

    def test_raises_exception_if_subject_pref_unit_is_undefined(self):
        qo = model.quantity.QuantityOf(
            subject=fx.SupportsExtendedUnitsTestable(g_per_ml=None),
            quantity_data_src=fx.get_qty_data_src(qty_in_g=1.2, pref_unit='L')
        )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            _ = qo.persistable_data
