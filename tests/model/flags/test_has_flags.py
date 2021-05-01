from unittest import TestCase

import model


class TestGetFlagValue(TestCase):
    def setUp(self) -> None:
        self.ingredient = model.ingredients.Ingredient()
        self.ingredient.set_nutrient_ratio(
            nutrient_name="alcohol",
            nutrient_qty=0,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )
        self.ingredient.set_flag_value("vegan", True)

    def test_gets_single_nutrient_direct_alias_correctly(self) -> None:
        self.assertTrue(self.ingredient.get_flag_value("alcohol_free"))

    def test_gets_unrelated_non_direct_alias_correctly(self) -> None:
        self.assertTrue(self.ingredient.get_flag_value("vegan"))

    def test_flag_values_start_as_undefined(self) -> None:
        i = model.ingredients.Ingredient()
        for flag_name in model.flags.ALL_FLAG_NAMES:
            with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
                _ = i.get_flag_value(flag_name)
