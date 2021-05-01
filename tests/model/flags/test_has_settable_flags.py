from unittest import TestCase

import model.exceptions
from model import ingredients, flags


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
        # Check we get a fixable nr error if we don't pass the modify flag;
        with self.assertRaises(model.exceptions.FixableNutrientRatioConflictError):
            self.ingredient.set_flag_value(
                flag_name="alcohol_free",
                flag_value=True
            )
        # Check we get no error if we do pass the modify flag;
        self.ingredient.set_flag_value(
            flag_name="alcohol_free",
            flag_value=True,
            can_modify_nutrients=True
        )
        self.assertTrue(self.ingredient.get_flag_value("alcohol_free"))
        nr = self.ingredient.get_nutrient_ratio("alcohol")
        self.assertEqual(nr.g_per_subject_g, 0)
