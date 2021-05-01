from unittest import TestCase

import model


class TestSetNutrientRatio(TestCase):

    def setUp(self) -> None:
        self.ingredient = model.ingredients.Ingredient()

    def test_sets_nutrient_ratio_correctly(self):
        self.ingredient.set_nutrient_ratio(
            nutrient_name='protein',
            nutrient_qty=100,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )
        nr = self.ingredient.get_nutrient_ratio('protein')
        self.assertEqual(nr.g_per_subject_g, 1)

    def test_catches_nutrient_name_error(self):
        # Check you don't get an error if the name exists;
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name='made_up',
                nutrient_qty=100,
                nutrient_qty_unit='g',
                subject_qty=100,
                subject_qty_unit='g'
            )

    def test_catches_nutrient_qty_exceeds_parent_qty(self):
        with self.assertRaises(model.nutrients.exceptions.NutrientQtyExceedsSubjectQtyError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name="carbohydrate",
                nutrient_qty=30,
                nutrient_qty_unit='g',
                subject_qty=25,
                subject_qty_unit='g'
            )

    def test_catches_nutrient_qty_units_not_mass(self):
        with self.assertRaises(model.quantity.exceptions.IncorrectUnitTypeError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name="carbohydrate",
                nutrient_qty=30,
                nutrient_qty_unit='L',
                subject_qty=25,
                subject_qty_unit='g'
            )

    def test_catches_child_nutrients_exceed_parent_mass(self):
        self.ingredient.set_nutrient_ratio(
            nutrient_name="carbohydrate",
            nutrient_qty=0.8,
            nutrient_qty_unit='g',
            subject_qty=1,
            subject_qty_unit='g'
        )
        self.ingredient.set_nutrient_ratio(
            nutrient_name="glucose",
            nutrient_qty=0.5,
            nutrient_qty_unit='g',
            subject_qty=1,
            subject_qty_unit='g'
        )
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name="fructose",
                nutrient_qty=0.4,
                nutrient_qty_unit='g',
                subject_qty=1,
                subject_qty_unit='g'
            )

    def test_prevents_zero_subject_mass(self):
        with self.assertRaises(model.quantity.exceptions.ZeroQtyError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name="carbohydrate",
                nutrient_qty=0,
                nutrient_qty_unit='g',
                subject_qty=0,
                subject_qty_unit='g'
            )