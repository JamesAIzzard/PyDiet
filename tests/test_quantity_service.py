from unittest import TestCase

from pydiet import quantity

class TestConvertQtyUnit(TestCase):

    def setUp(self) -> None:
        self.g_per_ml = 1.2
        self.piece_mass_g = 100

    def test_converts_mass_to_mass_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=2,
            start_unit='kg',
            end_unit='lb' 
        )
        self.assertAlmostEqual(result, 4.409, delta=0.001)

    def test_converts_vol_to_vol_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=2,
            start_unit='L',
            end_unit='pint' 
        )
        self.assertAlmostEqual(result, 4.227, delta=0.001)

    def test_converts_mass_to_vol_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=2,
            start_unit='kg',
            end_unit='L',
            g_per_ml=self.g_per_ml
        )
        self.assertAlmostEqual(result, 20/12, delta=0.001)

    def test_converts_vol_to_mass_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=20/12,
            start_unit='L',
            end_unit='kg',
            g_per_ml=self.g_per_ml
        )
        self.assertAlmostEqual(result, 2, delta=0.001)

    def test_converts_pc_to_mass_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=1,
            start_unit='pc',
            end_unit='kg',
            piece_mass_g=self.piece_mass_g
        )
        self.assertAlmostEqual(result, 0.1, delta=0.001)

    def test_converts_mass_to_pc_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=1,
            start_unit='kg',
            end_unit='pc',
            piece_mass_g=self.piece_mass_g
        )
        self.assertAlmostEqual(result, 10, delta=0.001)

    def test_converts_pc_to_vol_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=2, # So 200g
            start_unit='pc',
            end_unit='L',
            piece_mass_g=self.piece_mass_g,
            g_per_ml=self.g_per_ml # So (200/1.2)ml, so ((200/1.2)/1000) L 
        )
        self.assertAlmostEqual(result, ((200/1.2)/1000), delta=0.001)

    def test_converts_vol_to_pc_correctly(self):
        result = quantity.quantity_service.convert_qty_unit(
            qty=(200/1.2)/1000,
            start_unit='L',
            end_unit='pc',
            piece_mass_g=self.piece_mass_g,
            g_per_ml=self.g_per_ml
        )
        self.assertAlmostEqual(result, 2, delta=0.001)

    def test_error_if_g_per_ml_missing(self):
        with self.assertRaises(ValueError):
            quantity.quantity_service.convert_qty_unit(
                qty = 2,
                start_unit='ml',
                end_unit='g'
            )
        with self.assertRaises(ValueError):
            quantity.quantity_service.convert_qty_unit(
                qty = 2,
                start_unit='kg',
                end_unit='L'
            )
        with self.assertRaises(ValueError):
            quantity.quantity_service.convert_qty_unit(
                qty = 2,
                start_unit='L',
                end_unit='pc',
                piece_mass_g=self.piece_mass_g
            )                           

    def test_error_if_piece_mass_g_missing(self):
        with self.assertRaises(ValueError):
            quantity.quantity_service.convert_qty_unit(
                qty = 2,
                start_unit='kg',
                end_unit='pc'
            )
        with self.assertRaises(ValueError):
            quantity.quantity_service.convert_qty_unit(
                qty = 2,
                start_unit='L',
                end_unit='pc',
                g_per_ml=self.g_per_ml
            )            

class TestConvertDensityUnit(TestCase):

    def test_converts_densities_correctly(self):
        g_per_ml = 5
        lb_per_L = quantity.quantity_service.convert_density_unit(g_per_ml, 'g', 'ml', 'lb', 'L')
        self.assertAlmostEqual(11.02, lb_per_L, delta=0.1)

    def test_converts_density_with_pc_unit_start_mass(self):
        pc_per_ml = 1.5
        piece_mass_g = 100
        lb_per_L = quantity.quantity_service.convert_density_unit(pc_per_ml, 'pc', 'ml', 'lb', 'L', piece_mass_g)
        self.assertAlmostEqual(330.7, lb_per_L, delta=0.1)        

    def test_converts_density_with_pc_unit_end_mass(self):
        piece_mass_g = 270
        pc_per_L = quantity.quantity_service.convert_density_unit(1.5, 'kg', 'ml', 'pc', 'L', piece_mass_g)
        self.assertAlmostEqual(pc_per_L, 1.5e6/270, delta=0.1)  