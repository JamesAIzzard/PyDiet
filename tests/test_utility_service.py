from pydiet.shared.exceptions import TimeIntervalParseError, TimeIntervalValueError
from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

import dependencies

if TYPE_CHECKING:
    from pydiet.shared import utility_service
    from pydiet.ingredients import ingredient_service


class TestParseNumberAndText(TestCase):
    def setUp(self):
        self.ut: 'utility_service' = inject('pydiet.utility_service')

    def test_parses_correctly(self):
        output = self.ut.parse_number_and_text('4kg')
        self.assertEqual(output, (4, 'kg'))

class TestParseTimeInterval(TestCase):
    def setUp(self):
        self.ut: 'utility_service' = inject('pydiet.utility_service')

    def test_parses_correctly(self):
        output = self.ut.parse_time_interval("06:00-10:00")
        self.assertEqual(output, "06:00-10:00")
    
    def test_corrects_single_digits(self):
        output = self.ut.parse_time_interval("6:00-10:00")
        self.assertEqual(output, "06:00-10:00")
        output = self.ut.parse_time_interval("11:00-9:5")
        self.assertEqual(output, "11:00-09:05")    

    def test_catches_impossible_times(self):
        with self.assertRaises(TimeIntervalValueError):
            self.ut.parse_time_interval("60:00-10:00")
        with self.assertRaises(TimeIntervalValueError):
            self.ut.parse_time_interval("9:00-25:00")

    def test_catches_one_ended_intervals(self):
        with self.assertRaises(TimeIntervalParseError):
            self.ut.parse_time_interval("11:00")

    def test_catches_nonsense_string_input(self):
        with self.assertRaises(TimeIntervalParseError):
            self.ut.parse_time_interval("alsdkjdagf")

    def test_catches_identical_time_endpoints(self):
        with self.assertRaises(TimeIntervalValueError):
            self.ut.parse_time_interval("9:00-9:00")

class TestScoreSimilarity(TestCase):
    def setUp(self):
        self.ut: 'utility_service' = inject('pydiet.utility_service')

    def test_scores_match_correctly(self):
        words = ["one", "two", "three", "four"]
        search_term = "one"
        score = self.ut.score_similarity(words, search_term)
        self.assertEqual(score["one"], 1.0)


class TestConvertVolumeUnits(TestCase):
    def setUp(self):
        self.ut: 'utility_service' = inject('pydiet.utility_service')

    def test_converts_volumes_correctly(self):
        start_vol_l = 1.2
        vol_ml = self.ut.convert_volume_units(start_vol_l, 'l', 'ml')
        vol_cm3 = self.ut.convert_volume_units(start_vol_l, 'l', 'cm3')
        vol_l = self.ut.convert_volume_units(start_vol_l, 'l', 'l')
        vol_m3 = self.ut.convert_volume_units(start_vol_l, 'l', 'm3')
        vol_quart = self.ut.convert_volume_units(start_vol_l, 'l', 'quart')
        vol_tsp = self.ut.convert_volume_units(start_vol_l, 'l', 'tsp')
        vol_tbsp = self.ut.convert_volume_units(start_vol_l, 'l', 'tbsp')
        self.assertEqual(vol_ml, 1200)
        self.assertEqual(vol_cm3, 1200)
        self.assertEqual(vol_l, 1.2)
        self.assertEqual(vol_m3, 0.0012)
        self.assertAlmostEqual(vol_quart, 1.27, delta=0.01)
        self.assertAlmostEqual(vol_tsp, 243, delta=1)
        self.assertAlmostEqual(vol_tbsp, 81.2, delta=0.1)


class TestConvertMassUnits(TestCase):
    def setUp(self):
        self.ut: 'utility_service' = inject('pydiet.utility_service')

    def test_converts_masses_correctly(self):
        start_mass_kg = 1.2
        mass_ug = self.ut.convert_mass_units(start_mass_kg, 'kg', 'ug')
        mass_mg = self.ut.convert_mass_units(start_mass_kg, 'kg', 'mg')
        mass_g = self.ut.convert_mass_units(start_mass_kg, 'kg', 'g')
        mass_kg = self.ut.convert_mass_units(start_mass_kg, 'kg', 'kg')
        self.assertEqual(mass_ug, 1.2e9)
        self.assertEqual(mass_mg, 1.2e6)
        self.assertEqual(mass_g, 1200)
        self.assertEqual(mass_kg, 1.2)


class TestConvertVolToMass(TestCase):
    def setUp(self):
        self.ut: 'utility_service' = inject('pydiet.utility_service')

    def test_converts_vol_to_mass_correctly(self):
        vol = 1.5
        vol_units = 'L'
        mass_units = 'mg'
        density_g_per_ml = 1.5
        mass_g = self.ut.convert_volume_to_mass(
            vol, vol_units, mass_units, density_g_per_ml
        )
        self.assertEqual(mass_g, 2.25e6)
