import unittest
from unittest import TestCase
from typing import TYPE_CHECKING

from pydiet.ingredients import ingredient_service
from pydiet.ingredients.ingredient import \
    ConstituentsExceedGroupError, Ingredient,
    ConstituentsExceedGroupError,
    DefinedByConstituentsError

class TestSetNutrientData(TestCase):
    def setUp(self):
        self.ingredient:'Ingredient' = ingredient_service.get_new_ingredient()

    def test_setting_molecule(self):
        self.ingredient.set_nutrient_data(
            "amylose", 1, 'g', 100, 'g'
        )
        am_data = self.ingredient.get_nutrient_data('amylose')
        self.assertEqual(am_data['ingredient_mass'], 100)
        self.assertEqual(am_data['ingredient_mass_units'], 'g')
        self.assertEqual(am_data['nutrient_mass'], 1)
        self.assertEqual(am_data['nutrient_mass_units'], 'g')

    def test_setting_group_directly(self):
        self.ingredient.set_nutrient_data(
            "vitamin_a", 1, 'g', 100, 'g'
        )
        va_data = self.ingredient.get_nutrient_data('vitamin_a')
        self.assertEqual(va_data['ingredient_mass'], 100)
        self.assertEqual(va_data['ingredient_mass_units'], 'g')
        self.assertEqual(va_data['nutrient_mass'], 1)
        self.assertEqual(va_data['nutrient_mass_units'], 'g')       

    def test_setting_group_by_constituents(self):
        # Set the constituents of vitamin a;
        self.ingredient.set_nutrient_data('retinol', 1, 'g', 100, 'g')
        self.ingredient.set_nutrient_data('retinal', 1, 'g', 100, 'g')
        self.ingredient.set_nutrient_data('retinoic_acid', 1, 'g', 100, 'g')
        self.ingredient.set_nutrient_data('b_carotene', 1, 'g', 100, 'g')
        # Ask for vitamin a data and check it matches
        va_data = self.ingredient.get_nutrient_data('vitamin_a')
        self.assertEqual(va_data['ingredient_mass'], 100)
        self.assertEqual(va_data['ingredient_mass_units'], 'g')
        self.assertEqual(va_data['nutrient_mass'], 4)
        self.assertEqual(va_data['nutrient_mass_units'], 'g')   

    def test_error_when_group_defined_by_constituents(self):
        # Fully define vit a by constituents;
        self.ingredient.set_nutrient_data('retinol', 1, 'g', 100, 'g')
        self.ingredient.set_nutrient_data('retinal', 1, 'g', 100, 'g')
        self.ingredient.set_nutrient_data('retinoic_acid', 1, 'g', 100, 'g')
        self.ingredient.set_nutrient_data('b_carotene', 1, 'g', 100, 'g')        
        with self.assertRaises(ConstituentsExceedGroupError):
            # Then try and set vitamin a directly;
            self.ingredient.set_nutrient_data('b_carotene', 1, 'g', 100, 'g')

    def test_error_when_setting_molecule_invalidates_group(self):
        pass