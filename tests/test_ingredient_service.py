from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

import dependencies

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service

class TestGetMatchingNutrientNames(TestCase):
    def test_returns_matching_names(self):
        ig:'ingredient_service' = inject('pydiet.ingredient_service')
        search_term = "protein"
        results = ig.get_matching_nutrient_names(search_term, 4)
        self.assertEqual(results[0], 'protein')

class TestSummariseDensity(TestCase):
    def setUp(self):
        self.igs:'ingredient_service' = inject('pydiet.ingredient_service')
        self.i = self.igs.load_new_ingredient()
    
    def test_returns_undefined(self):
        # Check the density is undefined to start with;
        self.assertEqual(self.igs.summarise_density(self.i), 'Undefined')
        # Set the density;
        self.i.set_density(1, 'L', 1, 'kg')
        # Check the summary now appears;
        print(self.igs.summarise_density(self.i))
        pass