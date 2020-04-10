# Add root module to path;
import sys
# sys.path.append('/home/james/Documents/PyDiet') # Ubuntu Desktop
sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet') # Work Laptop
# sys.path.append('C:\\Users\\James.Izzard\\Documents\\PyDiet') # Work Desktop

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

class TestSummarisePrimaryNutrients(TestCase):
    def test_summarises_nutrients(self):
        ig:'ingredient_service' = inject('pydiet.ingredient_service')
        i = ig.get_new_ingredient()
        i.set_nutrient_amount('protein', 1, 'kg', 65, 'g')
        i.set_nutrient_amount('sodium', 1, 'kg', 2, 'ug')
        i.set_nutrient_amount('fat', 1, 'kg', 0.2, 'g')
        s = ig.summarise_primary_nutrients(i)
        print(s)