from unittest import TestCase

from model import ingredients


class TestSetFlag(TestCase):

    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_sets_flag_without_relations(self) -> None:
        self.ingredient.set_flag_value(
            flag_name="vegan",
            flag_value=True
        )
        self.assertTrue(self.ingredient.get_flag_value("vegan"))

    def test_sets_flag_and_zeros_single_nutrient(self) -> None:
        self.ingredient.set_flag_value(
            flag_name="alcohol_free",
            flag_value=True
        )
        self.assertTrue(self.ingredient.get_flag_value("alcohol_free"))
        nr = self.ingredient.get_nutrient_ratio("alcohol")
        self.assertEqual(nr.g_per_subject_g, 0)
