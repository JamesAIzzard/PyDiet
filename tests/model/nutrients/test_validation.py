from unittest import TestCase

import model


class TestValidateNutrientName(TestCase):
    def test_returns_primary_name(self):
        self.assertTrue(
            model.nutrients.validation.validate_nutrient_name('protein') == 'protein'
        )

    def test_returns_alais_name(self):
        self.assertTrue(
            model.nutrients.validation.validate_nutrient_name('vitamin_b12') == 'vitamin_b12'
        )
