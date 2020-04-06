# Add root module to path;
import sys, os
# sys.path.append('/home/james/Documents/PyDiet')
sys.path.append('c:\\Users\\james.izzard\\Documents\\PyDiet')

from unittest import TestCase
from typing import TYPE_CHECKING

from pinjector import inject

import dependencies

if TYPE_CHECKING:
    from pydiet.ingredients import ingredient_service

from pydiet.ingredients.ingredient import (
    ConstituentsExceedGroupError, 
    Ingredient, 
    NutrientQtyExceedsIngredientQtyError
)

class TestIngredientInit(TestCase):
    def test_molecule_can_be_set(self):
        ig:'ingredient_service' = inject('pydiet.ingredient_service')
        i = ig.get_new_ingredient()
        i.set_nutrient_amount('sodium', 250, 'g', 2, 'g')
        s = i.get_nutrient_amount('sodium')
        s.nutrient_mass_g
        self.assertEqual(s.percentage, 0.8)
        self.assertEqual(s.nutrient_mass_g, 2)

    def test_group_can_be_set(self):
        ig:'ingredient_service' = inject('pydiet.ingredient_service')
        i = ig.get_new_ingredient()
        i.set_nutrient_amount('protein', 250, 'g', 0.1, 'kg')
        p = i.get_nutrient_amount('protein')
        p.nutrient_mass_g
        self.assertEqual(p.percentage, 40)
        self.assertEqual(p.nutrient_mass_g, 100)

    def test_constituents_exceed_group_error(self):
        ig:'ingredient_service' = inject('pydiet.ingredient_service')
        i = ig.get_new_ingredient()
        i.set_nutrient_amount('protein', 250, 'g', 0.1, 'kg')
        i.set_nutrient_amount('alanine', 250, 'g', 100, 'g')
        i.set_nutrient_amount('leucine', 250, 'g', 100, 'g')
        with self.assertRaises(ConstituentsExceedGroupError):
            i.set_nutrient_amount('glycine', 250, 'g', 100, 'g')

    # TODO - Test that error is raised if you set the nutrient
    # qty higher than the ingredient qty.