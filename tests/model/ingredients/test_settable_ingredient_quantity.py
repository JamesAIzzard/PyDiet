"""Tests for SettableIngredientQuantity class."""
from unittest import TestCase

import model
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor."""
    def test_can_create_instance(self):
        """Test we can create a simple instance."""
        # Create a simple instance;
        siq = model.ingredients.SettableIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_ingredient_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
                )
            ),
            quantity_data=qfx.get_qty_data()
        )

        # Assert it was created;
        self.assertTrue(isinstance(siq, model.ingredients.SettableIngredientQuantity))

    def test_exception_if_ingredient_is_writable(self):
        """Check that we can't instantiate with a writeable ingredient."""
        # Check we get a TypeError
        with self.assertRaises(TypeError):
            # noinspection PyTypeChecker
            _ = model.ingredients.SettableIngredientQuantity(
                ingredient=model.ingredients.SettableIngredient(
                    ingredient_data=ifx.get_ingredient_data(for_unique_name=ifx.get_ingredient_name_with(
                        "typical_fully_defined_data"
                    ))
                ),
                quantity_data=qfx.get_qty_data()
            )


class TestSetQuantity(TestCase):
    """Tests the set_quantity method."""
    def test_can_set_quantity(self):
        """Checks that we can set the quantity of the ingredient."""
        # Create a simple instance;
        siq = model.ingredients.SettableIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_ingredient_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
                )
            ),
            quantity_data=qfx.get_qty_data()
        )

        # Assert that the quantity is not defined;
        self.assertFalse(siq.quantity_is_defined)

        # Set the quantity;
        siq.set_quantity(
            quantity_value=0.1,
            quantity_unit="kg"
        )

        # Assert that the quantity has been set;
        self.assertTrue(siq.quantity_is_defined)
        self.assertEqual(100, siq.quantity_in_g)

    def test_can_set_quantity_with_extended_units_if_configured(self):
        """Checks that we can use extended units to set the ingredient quantity if the ingredient
        has extended units configured."""
        # Create a test instance with extended units configured;
        siq = model.ingredients.SettableIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_ingredient_unique_name=ifx.get_ingredient_name_with("density_defined")
                )
            ),
            quantity_data=qfx.get_qty_data()
        )

        # Assert that the quantity is not defined;
        self.assertFalse(siq.quantity_is_defined)

        # Set the quantity;
        siq.set_quantity(
            quantity_value=1.2,
            quantity_unit="L"
        )

        # Assert that the quantity has been set;
        self.assertTrue(siq.quantity_is_defined)

    def test_cant_set_quantity_with_extended_units_if_not_configured(self):
        """Checks that we can't set quantity with extended units if they are not configured."""
        # Create a test instance without extended units.
        siq = model.ingredients.SettableIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_ingredient_unique_name=ifx.get_ingredient_name_with("density_undefined")
                )
            ),
            quantity_data=qfx.get_qty_data()
        )

        # Assert we get an exception if we try to use extended units;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            siq.set_quantity(quantity_value=1.2, quantity_unit="L")


class TestNumCalories(TestCase):
    """Tests the num_calories property in the context of the SettableIngredientQuantity class."""
    def check_num_calories_doubles_if_quantity_is_doubled(self):
        """Checks that the number of calories doubles if we double the quantity of ingredient."""
        # Create a test instance of defined quantity;
        siq = model.ingredients.SettableIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_ingredient_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
                )
            ),
            quantity_data=qfx.get_qty_data(qty_in_g=150)
        )

        # Record the number of calories;
        num_cals = siq.num_calories

        # Double the quantity;
        siq.set_quantity(quantity_value=300, quantity_unit='g')

        # Assert the number of calories has doubled;
        self.assertEqual(num_cals * 2, siq.num_calories)


class TestIngredient(TestCase):
    """Test the subject property."""
    def test_cant_mess_with_ingredient_attributes(self):
        """Checks that the ingredient is not mutable in this context."""
        # Create a test instance;
        siq = model.ingredients.SettableIngredientQuantity(
            ingredient=model.ingredients.ReadonlyIngredient(
                ingredient_data_src=ifx.get_ingredient_data_src(
                    for_ingredient_unique_name=ifx.get_ingredient_name_with("typical_fully_defined_data")
                )
            ),
            quantity_data=qfx.get_qty_data(qty_in_g=150)
        )

        # Check we get an exception if we try to mess with an ingredient property;
        with self.assertRaises(AttributeError):
            # noinspection PyPropertyAccess
            siq.ingredient.name = "Another Name"
