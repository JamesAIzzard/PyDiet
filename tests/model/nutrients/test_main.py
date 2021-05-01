from unittest import TestCase

import model


class TestGetNutrientPrimaryName(TestCase):
    def test_primary_name_is_returned_if_no_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('protein') == 'protein')

    def test_primary_name_is_returned_from_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('vitamin_b12') == 'cobalamin')
