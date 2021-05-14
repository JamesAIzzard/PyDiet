from unittest import TestCase

import model


class TestUnitsAreMasses(TestCase):
    def test_returns_true_if_all_units_are_masses(self):
        self.assertTrue(model.quantity.units_are_masses("kg", "g", "mg"))

    def test_returns_false_if_unit_is_not_a_mass(self):
        self.assertFalse(model.quantity.units_are_masses("kg", "l", "g"))


class TestUnitsAreVolumes(TestCase):
    def test_returns_true_if_all_units_are_volumes(self):
        self.assertTrue(model.quantity.units_are_volumes("l", "tbsp", "ml"))

    def test_returns_false_if_unit_is_not_volume(self):
        self.assertFalse(model.quantity.units_are_volumes("l", "kg", "ml"))


class TestUnitsArePieces(TestCase):
    def test_returns_true_if_all_units_are_pieces(self):
        self.assertTrue(model.quantity.units_are_pieces("pc"))

    def test_returns_false_if_unit_is_not_piece(self):
        self.assertFalse(model.quantity.units_are_pieces("kg", "pc"))


class TestUnitIsExtended(TestCase):
    def test_returns_true_if_unit_is_extended(self):
        self.assertTrue(model.quantity.unit_is_extended("l"))
        self.assertTrue(model.quantity.unit_is_extended("pc"))

    def test_returns_false_if_unit_is_not_extended(self):
        self.assertFalse(model.quantity.unit_is_extended("g"))
        self.assertFalse(model.quantity.unit_is_extended("kg"))

    def test_raises_exception_if_unit_not_recognised(self):
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            _ = model.quantity.unit_is_extended("fake")


class TestConvertLike2Like(TestCase):
    def test_converts_g_to_kg_correctly(self):
        self.assertEqual(model.quantity.main._convert_like2like(
            qty=3000,
            start_unit='g',
            end_unit='kg'
        ), 3)

    def test_converts_l_to_ml_correctly(self):
        self.assertEqual(model.quantity.main._convert_like2like(
            qty=3,
            start_unit='l',
            end_unit='ml'
        ), 3000)

    def test_raises_exception_if_unit_unknown(self):
        with self.assertRaises(model.quantity.exceptions.UnknownUnitError):
            _ = model.quantity.main._convert_like2like(
                qty=3,
                start_unit="l",
                end_unit='fake'
            )

    def test_raises_exception_if_units_not_alike(self):
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            _ = model.quantity.main._convert_like2like(
                qty=3,
                start_unit="L",
                end_unit="kg"
            )


class TestConvertMassAndVol(TestCase):
    def test_converts_kg_to_l_correctly(self):
        self.assertEqual(model.quantity.main._convert_mass_and_vol(
            qty=3,
            start_unit='kg',
            end_unit='l',
            g_per_ml=0.75
        ), 4)

    def test_converts_l_to_g_correctly(self):
        self.assertEqual(model.quantity.main._convert_mass_and_vol(
            qty=4,
            start_unit='l',
            end_unit='g',
            g_per_ml=0.75
        ), 3000)

    def test_raises_exception_if_both_units_alike(self):
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            _ = model.quantity.main._convert_mass_and_vol(
                qty=4,
                start_unit='kg',
                end_unit='g',
                g_per_ml=0.75
            )


class TestConvertPcAndMass(TestCase):
    def test_converts_pc_to_mass_correctly(self):
        self.assertEqual(model.quantity.main._convert_pc_and_mass(
            qty=2,
            start_unit='pc',
            end_unit='kg',
            piece_mass_g=1.5
        ), 0.003)

    def test_converts_mass_to_pc_correctly(self):
        self.assertEqual(model.quantity.main._convert_pc_and_mass(
            qty=3,
            start_unit='g',
            end_unit='pc',
            piece_mass_g=1.5
        ), 2)


class TestConvertPcAndVol(TestCase):
    def test_converts_pc_to_vol_correctly(self):
        self.assertEqual(model.quantity.main._convert_pc_and_vol(
            qty=2,
            start_unit='pc',
            end_unit='L',
            piece_mass_g=1.5,
            g_per_ml=1.2
        ), 0.0025)

    def test_converts_vol_to_pc_correctly(self):
        self.assertEqual(model.quantity.main._convert_pc_and_vol(
            qty=0.0025,
            start_unit='L',
            end_unit='pc',
            piece_mass_g=1.5,
            g_per_ml=1.2
        ), 2)


class TestConvertQtyUnit(TestCase):

    def setUp(self) -> None:
        self.g_per_ml = 1.2
        self.piece_mass_g = 100

    def test_converts_mass_to_mass_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=2,
            start_unit='kg',
            end_unit='lb'
        )
        self.assertAlmostEqual(result, 4.409, delta=0.001)

    def test_converts_vol_to_vol_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=2,
            start_unit='L',
            end_unit='pint'
        )
        self.assertAlmostEqual(result, 4.227, delta=0.001)

    def test_converts_mass_to_vol_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=2,
            start_unit='kg',
            end_unit='L',
            g_per_ml=self.g_per_ml
        )
        self.assertAlmostEqual(result, 20 / 12, delta=0.001)

    def test_converts_vol_to_mass_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=20 / 12,
            start_unit='L',
            end_unit='kg',
            g_per_ml=self.g_per_ml
        )
        self.assertAlmostEqual(result, 2, delta=0.001)

    def test_converts_pc_to_mass_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=1,
            start_unit='pc',
            end_unit='kg',
            piece_mass_g=self.piece_mass_g
        )
        self.assertAlmostEqual(result, 0.1, delta=0.001)

    def test_converts_mass_to_pc_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=1,
            start_unit='kg',
            end_unit='pc',
            piece_mass_g=self.piece_mass_g
        )
        self.assertAlmostEqual(result, 10, delta=0.001)

    def test_converts_pc_to_vol_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=2,  # So 200g
            start_unit='pc',
            end_unit='L',
            piece_mass_g=self.piece_mass_g,
            g_per_ml=self.g_per_ml  # So (200/1.2)ml, so ((200/1.2)/1000) L
        )
        self.assertAlmostEqual(result, ((200 / 1.2) / 1000), delta=0.001)

    def test_converts_vol_to_pc_correctly(self):
        result = model.quantity.main.convert_qty_unit(
            qty=(200 / 1.2) / 1000,
            start_unit='L',
            end_unit='pc',
            piece_mass_g=self.piece_mass_g,
            g_per_ml=self.g_per_ml
        )
        self.assertAlmostEqual(result, 2, delta=0.001)

    def test_error_if_g_per_ml_missing(self):
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            model.quantity.main.convert_qty_unit(
                qty=2,
                start_unit='ml',
                end_unit='g'
            )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            model.quantity.main.convert_qty_unit(
                qty=2,
                start_unit='kg',
                end_unit='L'
            )
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            model.quantity.main.convert_qty_unit(
                qty=2,
                start_unit='L',
                end_unit='pc',
                piece_mass_g=self.piece_mass_g
            )

    def test_error_if_piece_mass_g_missing(self):
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            model.quantity.main.convert_qty_unit(
                qty=2,
                start_unit='kg',
                end_unit='pc'
            )
        with self.assertRaises(model.quantity.exceptions.UndefinedPcMassError):
            model.quantity.main.convert_qty_unit(
                qty=2,
                start_unit='L',
                end_unit='pc',
                g_per_ml=self.g_per_ml
            )


class TestConvertDensityUnit(TestCase):

    def test_converts_densities_correctly(self):
        g_per_ml = 5
        lb_per_l = model.quantity.main.convert_density_unit(g_per_ml, 'g', 'ml', 'lb', 'L')
        self.assertAlmostEqual(11.02, lb_per_l, delta=0.1)

    def test_converts_density_with_pc_unit_start_mass(self):
        pc_per_ml = 1.5
        piece_mass_g = 100
        lb_per_l = model.quantity.main.convert_density_unit(pc_per_ml, 'pc', 'ml', 'lb', 'L', piece_mass_g)
        self.assertAlmostEqual(330.7, lb_per_l, delta=0.1)

    def test_converts_density_with_pc_unit_end_mass(self):
        piece_mass_g = 270
        pc_per_l = model.quantity.main.convert_density_unit(1.5, 'kg', 'ml', 'pc', 'L', piece_mass_g)
        self.assertAlmostEqual(pc_per_l, 1.5e6 / 270, delta=0.1)
