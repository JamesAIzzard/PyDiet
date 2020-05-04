import sys
# sys.path.append('/home/james/Documents/PyDiet') # Ubuntu Desktop
# sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet') # Work Laptop
sys.path.append('C:\\Users\\James.Izzard\\Documents\\PyDiet') # Work Desktop

from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

import dependencies

if TYPE_CHECKING:
    from pydiet.shared import utility_service

class TestParseNumberAndUnits(TestCase):
    def setUp(self):
        self.ut:'utility_service' = inject('pydiet.utility_service')

    def test_parses_correctly(self):
        output = self.ut.parse_number_and_units('4kg')
        self.assertEqual(output, (4, 'kg'))

class TestScoreSimilarity(TestCase):
    def setUp(self):
        self.ut:'utility_service' = inject('pydiet.utility_service')

    def test_scores_match_correctly(self):
        words = ["one", "two", "three", "four"]
        search_term = "one"
        score = self.ut.score_similarity(words, search_term)
        self.assertEqual(score["one"], 1.0)

class TestConvertVolume(TestCase):
    def setUp(self):
        self.ut:'utility_service' = inject('pydiet.utility_service')

    def test_converts_volumes_correctly(self):
        start_vol_l = 1.2
        vol_ml = self.ut.convert_volume(start_vol_l, 'l', 'ml')
        vol_cm3 = self.ut.convert_volume(start_vol_l, 'l', 'cm3')
        vol_l = self.ut.convert_volume(start_vol_l, 'l', 'l')
        vol_m3 = self.ut.convert_volume(start_vol_l, 'l', 'm3')
        vol_quart = self.ut.convert_volume(start_vol_l, 'l', 'quart')
        vol_tsp = self.ut.convert_volume(start_vol_l, 'l', 'tsp')
        vol_tbsp = self.ut.convert_volume(start_vol_l, 'l', 'tbsp')
        self.assertEqual(vol_ml, 1200)
        self.assertEqual(vol_cm3, 1200)
        self.assertEqual(vol_l, 1.2)
        self.assertEqual(vol_m3, 0.0012)
        self.assertAlmostEqual(vol_quart, 1.27, delta=0.01)
        self.assertAlmostEqual(vol_tsp, 243, delta=1)
        self.assertAlmostEqual(vol_tbsp, 81.2, delta=0.1)

class TestConvertMass(TestCase):
    def setUp(self):
        self.ut:'utility_service' = inject('pydiet.utility_service')

    def test_converts_masses_correctly(self):
        start_mass_kg = 1.2
        mass_ug = self.ut.convert_mass(start_mass_kg, 'kg', 'ug')
        mass_mg = self.ut.convert_mass(start_mass_kg, 'kg', 'mg')
        mass_g = self.ut.convert_mass(start_mass_kg, 'kg', 'g')
        mass_kg = self.ut.convert_mass(start_mass_kg, 'kg', 'kg')
        self.assertEqual(mass_ug, 1.2e9)
        self.assertEqual(mass_mg, 1.2e6)
        self.assertEqual(mass_g, 1200)
        self.assertEqual(mass_kg, 1.2)