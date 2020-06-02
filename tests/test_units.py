from unittest import TestCase

from pydiet import units

class TestConvertVolumeUnits(TestCase):

    def test_converts_volumes_correctly(self):
        start_vol_l = 1.2
        vol_ml = units.convert_volume_units(start_vol_l, 'l', 'ml')
        vol_cm3 = units.convert_volume_units(start_vol_l, 'l', 'cm3')
        vol_l = units.convert_volume_units(start_vol_l, 'l', 'l')
        vol_m3 = units.convert_volume_units(start_vol_l, 'l', 'm3')
        vol_quart = units.convert_volume_units(start_vol_l, 'l', 'quart')
        vol_tsp = units.convert_volume_units(start_vol_l, 'l', 'tsp')
        vol_tbsp = units.convert_volume_units(start_vol_l, 'l', 'tbsp')
        self.assertEqual(vol_ml, 1200)
        self.assertEqual(vol_cm3, 1200)
        self.assertEqual(vol_l, 1.2)
        self.assertEqual(vol_m3, 0.0012)
        self.assertAlmostEqual(vol_quart, 1.27, delta=0.01)
        self.assertAlmostEqual(vol_tsp, 243, delta=1)
        self.assertAlmostEqual(vol_tbsp, 81.2, delta=0.1)


class TestConvertMassUnits(TestCase):

    def test_converts_masses_correctly(self):
        start_mass_kg = 1.2
        mass_ug = units.convert_mass_units(start_mass_kg, 'kg', 'ug')
        mass_mg = units.convert_mass_units(start_mass_kg, 'kg', 'mg')
        mass_g = units.convert_mass_units(start_mass_kg, 'kg', 'g')
        mass_kg = units.convert_mass_units(start_mass_kg, 'kg', 'kg')
        self.assertEqual(mass_ug, 1.2e9)
        self.assertEqual(mass_mg, 1.2e6)
        self.assertEqual(mass_g, 1200)
        self.assertEqual(mass_kg, 1.2)


class TestConvertVolToMass(TestCase):

    def test_converts_vol_to_mass_correctly(self):
        vol = 1.5
        vol_units = 'L'
        mass_units = 'mg'
        density_g_per_ml = 1.5
        mass_g = units.convert_volume_to_mass(
            vol, vol_units, mass_units, density_g_per_ml
        )
        self.assertEqual(mass_g, 2.25e6)