"""Ingredient class tests."""
from unittest import TestCase

import model
import persistence
from tests.model.ingredients import fixtures as fx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Constructor method tests."""

    @pfx.use_test_database
    def test_can_create_instance(self):
        """Check we can initialise an instance."""
        # First, create the instance;
        i_name = "Honey"
        i = model.ingredients.ReadonlyIngredient(ingredient_data_src=fx.get_ingredient_data_src(i_name))

        # Now load the instance's data directly;
        data = fx.get_ingredient_data(for_unique_name=i_name)

        # Check that the instance data matches the data in the database;
        self.assertEqual(data, i.persistable_data)


# noinspection PyPep8Naming
class Test_GPerMl(TestCase):
    @pfx.use_test_database
    def test_returns_correct_value_if_defined(self):
        """Check that the property returns the correct value."""
        # Create a test instance of an ingredient with g_per_ml populated;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("density_defined")
            )
        )

        # Check the g_per_ml is correct;
        self.assertEqual(0.9736, i._g_per_ml)

    @pfx.use_test_database
    def test_returns_none_if_undefined(self):
        """Check that the property returns None if undefined;
        Since this is the private method, it returns None
        """
        # Create a test instance of an ingredient with g_per_ml undefined;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("density_undefined")
            )
        )

        # Check the return value is None;
        self.assertIsNone(i._g_per_ml)


# noinspection PyPep8Naming
class Test_PieceMassG(TestCase):
    """Tests the functionality of the Ingredient class' _piece_mass_g property."""

    @pfx.use_test_database
    def test_returns_correct_value_if_defined(self):
        """Check that the property returns the correct value."""
        # Create a test instance of an ingredient with piece mass populated;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("piece_mass_defined")
            )
        )

        # Check the g_per_ml is correct;
        self.assertEqual(300, i._piece_mass_g)

    @pfx.use_test_database
    def test_returns_none_if_undefined(self):
        """Check that the property returns None if undefined;
        Since this is the private method, it returns None
        """
        # Create a test instance of an ingredient with piece_mass undefined;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("piece_mass_undefined")
            )
        )

        # Check the return value is None;
        self.assertIsNone(i._piece_mass_g)


# noinspection PyPep8Naming
class Test_CostPerQtyData(TestCase):
    """Tests the _cost_per_qty_data property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_data_if_defined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("cost_per_g_defined")
            )
        )

        # Check the values are correct;
        self.assertEqual(0.002, i.cost_per_qty_data['cost_per_g'])
        self.assertEqual("g", i.cost_per_qty_data['pref_unit'])
        self.assertEqual(100, i.cost_per_qty_data['quantity_in_g'])

    @pfx.use_test_database
    def test_returns_correct_data_if_undefined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("cost_per_g_undefined")
            )
        )

        # Check the values are correct;
        self.assertIsNone(i.cost_per_qty_data['cost_per_g'])
        self.assertEqual("g", i.cost_per_qty_data['pref_unit'])
        self.assertIsNone(i.cost_per_qty_data['quantity_in_g'])


# noinspection PyPep8Naming
class Test_FlagDOFs(TestCase):
    """Tests the _flag_dofs property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_data_if_defined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("flag_dofs_all_defined")
            )
        )

        # Check the values are correct;
        self.assertTrue(i.flag_dofs['nut_free'])
        self.assertFalse(i.flag_dofs['vegan'])
        self.assertTrue(i.flag_dofs['vegetarian'])

    @pfx.use_test_database
    def test_returns_correct_data_if_undefined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("flag_dofs_two_undefined")
            )
        )

        # Check the values are correct;
        self.assertIsNone(i.flag_dofs['nut_free'])
        self.assertTrue(i.flag_dofs['vegan'])
        self.assertIsNone(i.flag_dofs['vegetarian'])


# noinspection PyPep8Naming
class Test_NutrientRatiosData(TestCase):
    """Tests the _nutrient_ratios_data property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_data_for_defined_nutrient_ratios(self):
        """Checks we get the correct data back for defined nutrient ratios."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("nutrient_ratios_protein_defined")
            )
        )

        # Check that there is a heading for protein;
        self.assertTrue("protein" in i.nutrient_ratios_data.keys())

        # Check the data is correct;
        self.assertEqual(18.82, i.nutrient_ratios_data['protein']['nutrient_mass_data']['quantity_in_g'])
        self.assertEqual("g", i.nutrient_ratios_data['protein']['nutrient_mass_data']['pref_unit'])
        self.assertEqual(100, i.nutrient_ratios_data['protein']['subject_ref_qty_data']['quantity_in_g'])
        self.assertEqual("g", i.nutrient_ratios_data['protein']['subject_ref_qty_data']['pref_unit'])

    @pfx.use_test_database
    def test_excludes_undefined_nutrients(self):
        """Checks undefined nutrients do not show up in the nutrient data dict."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("nutrient_ratios_iron_undefined")
            )
        )

        # Check that there is no heading for iron;
        self.assertFalse("iron" in i.nutrient_ratios_data.keys())

    @pfx.use_test_database
    def test_correct_number_nutrients_included(self):
        """Checks that the correct number of nutrients show up in the data dict."""
        # Create the test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("nutrient_ratios_8_ratios_defined")
            )
        )

        # Check that there is no heading for iron;
        self.assertEqual(8, len(i.nutrient_ratios_data))


class TestGetPathIntoDB(TestCase):
    """Tests the get_path_into_db property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_path(self):
        """Check that the property returns the correct path."""
        # Create a test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("typical_fully_defined_data")
            )
        )

        # Check the db path is correct;
        self.assertEqual(f"{persistence.configs.path_into_db}/ingredients", i.get_path_into_db())


class TestUniqueValue(TestCase):
    """Tests the unique_value property on the Ingredient class."""

    def test_returns_unique_value_correctly(self):
        """Check that the property returns the unique value correctly."""
        # Create a test instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("name_raspberry")
            )
        )

        # Check the name returns the correct value;
        self.assertEqual("Raspberry", i.unique_value)


class TestPersistableData(TestCase):
    """Tests the persistable data property on the Ingredient class."""

    def test_returns_correct_data(self):
        """Checks that the correct persistable data is returned."""
        # First, create the instance;
        i = model.ingredients.ReadonlyIngredient(
            ingredient_data_src=fx.get_ingredient_data_src(
                fx.get_ingredient_name_with("typical_fully_defined_data")
            )
        )

        # Now load the instance's data directly;
        data = fx.get_ingredient_data(for_unique_name=fx.get_ingredient_name_with("typical_fully_defined_data"))

        # Check that the instance data matches the data in the database;
        self.assertEqual(data, i.persistable_data)
