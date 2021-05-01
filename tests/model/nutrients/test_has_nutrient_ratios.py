from unittest import TestCase

import model


class TestGetNutrientRatio(TestCase):
    def setUp(self) -> None:
        self.ingredient = model.ingredients.Ingredient()

    def test_raises_exception_if_nutrient_ratio_unset(self):
        with self.assertRaises(model.nutrients.exceptions.UndefinedNutrientRatioError):
            _ = self.ingredient.get_nutrient_ratio("carbohydrate")

    def test_cant_get_nutrient_ratio_and_set_it_directly(self):
        # Set it first;
        self.ingredient.set_nutrient_ratio(
            nutrient_name='carbohydrate',
            nutrient_qty=80,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )
        # Now grab it;
        carb = self.ingredient.get_nutrient_ratio('carbohydrate')
        # Check that setting its properties directly raises exceptions;
        with self.assertRaises(AttributeError):
            carb.g_per_subject_g = 0.5  # noqa
        with self.assertRaises(AttributeError):
            carb.pref_unit = 'g'  # noqa
