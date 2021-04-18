from unittest import TestCase

from model import ingredients


class TestGetFlagValue(TestCase):
    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()
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

    def test_flag_value_starts_as_undefined(self) -> None:
        i = ingredients.Ingredient()
        for flag_name, flag_value in i.all_flag_values.items():
            self.assertEqual(flag_value, None)