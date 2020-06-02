from unittest import TestCase

from pydiet.ingredients import ingredient_service as igs
from pydiet.ingredients.exceptions import (
    ConstituentsExceedGroupError, 
    NutrientQtyExceedsIngredientQtyError
)

class TestSettingNutrients(TestCase):
    def setUp(self):
        self.i = igs.load_new_ingredient()

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
        self.i.set_nutrient_amount('alanine', 250, 'g', 40, 'g')
        self.i.set_nutrient_amount('leucine', 250, 'g', 40, 'g')
        with self.assertRaises(ConstituentsExceedGroupError):
            self.i.set_nutrient_amount('glycine', 250, 'g', 40, 'g')

    def test_nutrient_qty_exceeds_ingredient_qty_error(self):
        with self.assertRaises(NutrientQtyExceedsIngredientQtyError):
            self.i.set_nutrient_amount('fat', 10, 'g', 20, 'g')