"""Tests for the ReadonlyIngredinetQuantity class."""
from unittest import TestCase

import model
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_instance_can_be_created(self):
        """Checks that we can create a simple instance without error."""
        self.assertTrue(isinstance(
            model.ingredients.ReadonlyIngredientQuantity(
                ingredient=model.ingredients.ReadonlyIngredient(
                    ingredient_data_src=ifx.get_ingredient_data_src(
                        for_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
                    )
                ),
                quantity_data_src=qfx.get_qty_data_src(
                    quantity_data=qfx.get_qty_data()
                )
            ),
            model.ingredients.ReadonlyIngredientQuantity
        ))

    def test_exception_if_ingredient_is_writable(self):
        """Checks that we can't instantiate with a writable ingredient."""
        # Check we get a TypeError
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            _ = model.ingredients.SettableIngredientQuantity(
                ingredient=model.ingredients.SettableIngredient(
                    ingredient_data=ifx.get_ingredient_data(for_unique_name=ifx.get_ingredient_name_with(
                        "typical_fully_defined_data"
                    ))
                ),
                quantity_data_src=qfx.get_qty_data_src(quantity_data=qfx.get_qty_data())
            )


class TestIngredient(TestCase):
    """Tests the ingredient property."""

    def test_correct_ingredient_is_returned(self):
        """Checks that the correct ingredient instance is returned."""
        # Create a readonly ingredient;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=ifx.get_ingredient_data_src(
                for_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
            )
        )

        # Create an ReadableIngredientQuantity, passing the ingredient in;
        iq = model.ingredients.ReadonlyIngredientQuantity(
            ingredient=i,
            quantity_data_src=qfx.get_qty_data_src(
                quantity_data=qfx.get_qty_data()
            )
        )

        # Assert the ingredient we get out is the same as we passed in;
        self.assertTrue(i is iq.ingredient)


class TestRefQty(TestCase):
    """Tests the ref_qty property in the context of ingredient."""

    def test_returns_correct_ref_qty(self):
        """Checks that the method returns the correct reference quantity."""
        # Create an ReadableIngredientQuantity, passing quantity data in;
        # Create an ReadableIngredientQuantity, passing the mock ingredient in;
        iq = model.ingredients.ReadonlyIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
                )
            ),
            quantity_data_src=qfx.get_qty_data_src(
                quantity_data=qfx.get_qty_data(
                    qty_in_g=120,
                    pref_unit="lb"
                )
            )
        )

        # Assert that the correct reference quantity is returned;
        self.assertAlmostEqual(0.2646, iq.ref_qty, delta=0.001)


class TestGetNutrientMass(TestCase):
    """Tests the get_nutrient_mass property on the ReadableIngredientQuantity class."""

    @pfx.use_test_database
    def test_returns_the_correct_nutrient_mass(self):
        """Checks the method returns the correct nutrient mass."""
        # Create a test instance with a known ratio of a nutrient;
        iq = model.ingredients.ReadonlyIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=model.ingredients.get_ingredient_data_src(
                    for_unique_name=ifx.get_ingredient_name_with("14_grams_of_protein_per_100_g")
                )
            ),
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(
                qty_in_g=50
            ))
        )

        # Assert that we get the correct mass of that nutrient back, for a given quantity;
        self.assertAlmostEqual(7, iq.get_nutrient_mass_g("protein"), delta=0.001)


class TestNumCalories(TestCase):
    """Tests the num_calories property on the ReadableIngredientQuantity class."""

    @pfx.use_test_database
    def test_returns_the_correct_number_of_calories(self):
        """Checks that the method returns the correct number of calories."""
        # Create a test instance of an ingrediet with defined qty;
        iq = model.ingredients.ReadonlyIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=model.ingredients.get_ingredient_data_src(
                    for_unique_name=ifx.get_ingredient_name_with("7.2_calories_per_g")
                )
            ),
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(
                qty_in_g=120
            ))
        )

        # Check we get the correct number of calories
        self.assertAlmostEqual(864, iq.num_calories, delta=0.001)
