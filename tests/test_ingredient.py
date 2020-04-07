# Add root module to path;
import sys
# sys.path.append('/home/james/Documents/PyDiet') # Ubuntu Desktop
# sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet') # Work Laptop
sys.path.append('C:\\Users\\James.Izzard\\Documents\\PyDiet') # Work Desktop

from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

import dependencies

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service

from pydiet.ingredients.ingredient import (
    ConstituentsExceedGroupError, 
    NutrientQtyExceedsIngredientQtyError
)

class TestIngredientInit(TestCase):
    def setUp(self):
        ig:'ingredient_service' = inject('pydiet.ingredient_service')
        self.i = ig.get_new_ingredient()

    def test_molecule_can_be_set(self):
        self.i.set_nutrient_amount('sodium', 250, 'g', 2, 'g')
        s = self.i.get_nutrient_amount('sodium')
        s.nutrient_mass_g
        self.assertEqual(s.percentage, 0.8)
        self.assertEqual(s.nutrient_mass_g, 2)

    def test_group_can_be_set(self):
        self.i.set_nutrient_amount('protein', 250, 'g', 0.1, 'kg')
        p = self.i.get_nutrient_amount('protein')
        p.nutrient_mass_g
        self.assertEqual(p.percentage, 40)
        self.assertEqual(p.nutrient_mass_g, 100)

    def test_constituents_exceed_group_error(self):
        self.i.set_nutrient_amount('protein', 250, 'g', 0.1, 'kg')
        self.i.set_nutrient_amount('alanine', 250, 'g', 100, 'g')
        self.i.set_nutrient_amount('leucine', 250, 'g', 100, 'g')
        with self.assertRaises(ConstituentsExceedGroupError):
            self.i.set_nutrient_amount('glycine', 250, 'g', 100, 'g')

    def test_nutrient_qty_exceeds_ingredient_qty_error(self):
        with self.assertRaises(NutrientQtyExceedsIngredientQtyError):
            self.i.set_nutrient_amount('fat', 10, 'g', 20, 'g')