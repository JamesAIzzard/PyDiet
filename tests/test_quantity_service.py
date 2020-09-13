from unittest import TestCase

from pydiet import quantity

class TestConvertQtyUnit(TestCase):
    
    def test_converts_mass_to_mass_correctly(self):
        qty_lb = 5
        qty_g = quantity.quantity_service.convert_qty_unit(qty_lb, 'lb', 'g')
        self.assertAlmostEqual(2268, qty_g, delta=0.1)

        rho = 1.2
        qty_lb = 5
        qty_g = quantity.quantity_service.convert_qty_unit(qty_lb, 'lb', 'g', rho)
        self.assertAlmostEqual(2268, qty_g, delta=0.1)        

    def test_converts_mass_to_vol_correctly(self):
        qty_kg = 5
        rho = 1.2
        qty_L = quantity.quantity_service.convert_qty_unit(qty_kg, 'kg', 'L', rho)
        self.assertAlmostEqual(6, qty_L, delta=0.1)     

    def test_converts_vol_to_mass_correctly(self):
        qty_L = 6
        rho = 1.2
        qty_kg = quantity.quantity_service.convert_qty_unit(qty_L, 'L', 'kg', rho)
        self.assertAlmostEqual(5, qty_kg, delta=0.1)

    def test_converts_vol_to_vol_correctly(self):
        qty_ml = 5000
        qty_L = quantity.quantity_service.convert_qty_unit(qty_ml, 'ml', 'L')
        self.assertAlmostEqual(5, qty_L, delta=0.1)

        rho = 1.2
        qty_ml = 5000
        qty_L = quantity.quantity_service.convert_qty_unit(qty_ml, 'ml', 'L', rho)
        self.assertAlmostEqual(5, qty_L, delta=0.1)        

    def test_fails_if_rho_missing(self):
        qty_kg = 5
        with self.assertRaises(TypeError):
            quantity.quantity_service.convert_qty_unit(qty_kg, 'kg', 'L')

class TestConvertDensityUnit(TestCase):

    def test_converts_densities_correctly(self):
        g_per_ml = 5
        lb_per_L = quantity.quantity_service.convert_density_unit(g_per_ml, 'g', 'ml', 'lb', 'L')
        self.assertAlmostEqual(11.02, lb_per_L, delta=0.1)
