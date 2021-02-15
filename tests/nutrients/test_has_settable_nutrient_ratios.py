from unittest import TestCase

from model import nutrients, quantity, ingredients


class TestSetNutrientRatio(TestCase):

    def setUp(self) -> None:
        self.ingredient = ingredients.Ingredient()

    def test_catches_nutrient_name_error(self):
        # Check you do get an error if the name doesn't exist;
        self.ingredient.set_nutrient_ratio(
            nutrient_name='protein',
            nutrient_qty=100,
            nutrient_qty_unit='g',
            subject_qty=100,
            subject_qty_unit='g'
        )
        # Check you don't get an error if the name exists;
        with self.assertRaises(nutrients.exceptions.NutrientNameError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name='made_up',
                nutrient_qty=100,
                nutrient_qty_unit='g',
                subject_qty=100,
                subject_qty_unit='g'
            )

    def test_catches_nutrient_qty_exceeds_parent_qty(self):
        with self.assertRaises(nutrients.exceptions.NutrientQtyExceedsSubjectQtyError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name="carbohydrate",
                nutrient_qty=30,
                nutrient_qty_unit='g',
                subject_qty=25,
                subject_qty_unit='g'
            )

    def test_catches_nutrient_qty_units_not_mass(self):
        with self.assertRaises(quantity.exceptions.IncorrectUnitTypeError):
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
        with self.assertRaises(nutrients.exceptions.ChildNutrientQtyExceedsParentNutrientQtyError):
            self.ingredient.set_nutrient_ratio(
                nutrient_name="fructose",
                nutrient_qty=0.4,
                nutrient_qty_unit='g',
                subject_qty=1,
                subject_qty_unit='g'
            )
