"""Ingredient class tests."""
from unittest import TestCase

import model
import persistence
from tests.model.ingredients import fixtures as fx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Constructor method tests."""

    @pfx.use_test_database
    def test_can_create_instance_from_unique_name(self):
        """Check we can initialise an instance from the unique name."""
        # First, create the instance;
        i_name = "Honey"
        i = model.ingredients.Ingredient(unique_name=i_name)

        # Now load the instance's data directly;
        fp = "{path_into_db}/{df_name}.json".format(
            path_into_db=model.ingredients.Ingredient.get_path_into_db(),
            df_name=persistence.main.get_datafile_name_for_unique_value(
                cls=model.ingredients.Ingredient,
                unique_value=i_name
            )
        )
        data = persistence.main._read_datafile(filepath=fp)

        # Check that the instance data matches the data in the database;
        self.assertEqual(data, i.persistable_data)

    @pfx.use_test_database
    def test_can_create_instance_from_datafile_name(self):
        """Check we can initialise the ingredient from the datafile name."""
        # First, create the instance;
        df_name = "1198a703-ae23-4303-9b21-dd8ef9d16548"
        i = model.ingredients.Ingredient(datafile_name=df_name)

        # Now load the instance's data directly;
        fp = "{path_into_db}/{df_name}.json".format(
            path_into_db=model.ingredients.Ingredient.get_path_into_db(),
            df_name=df_name
            )
        data = persistence.main._read_datafile(filepath=fp)

        # Check that the instance data matches the data in the database;
        self.assertEqual(data, i.persistable_data)

    @pfx.use_test_database
    def test_raises_exception_if_no_name_provided(self):
        """Check we get an exception if we try and initialise an ingredient without providing a name."""
        with self.assertRaises(ValueError):
            _ = model.ingredients.Ingredient()

    @pfx.use_test_database
    def test_raises_exception_if_name_not_recognised(self):
        """Check we get an exception if the ingredient name isn't recognised."""
        # Try to create a test instance for an ingredient which doesn't exist in the
        # database;
        with self.assertRaises(persistence.exceptions.UniqueValueNotFoundError):
            _ = model.ingredients.Ingredient(unique_name="Fake")


# noinspection PyPep8Naming
class Test_GPerMl(TestCase):
    @pfx.use_test_database
    def test_returns_correct_value_if_defined(self):
        """Check that the property returns the correct value."""
        # Create a test instance of an ingredient with g_per_ml populated;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("density_defined"))

        # Check the g_per_ml is correct;
        self.assertEqual(0.9736, i._g_per_ml)

    @pfx.use_test_database
    def test_returns_none_if_undefined(self):
        """Check that the property returns None if undefined;
        Since this is the private method, it returns None
        """
        # Create a test instance of an ingredient with g_per_ml undefined;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("density_undefined"))

        # Check the return value is None;
        self.assertIsNone(i._g_per_ml)


# noinspection PyPep8Naming
class Test_PieceMassG(TestCase):
    """Tests the functionality of the Ingredient class' _piece_mass_g property."""

    @pfx.use_test_database
    def test_returns_correct_value_if_defined(self):
        """Check that the property returns the correct value."""
        # Create a test instance of an ingredient with piece mass populated;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("piece_mass_defined"))

        # Check the g_per_ml is correct;
        self.assertEqual(300, i._piece_mass_g)

    @pfx.use_test_database
    def test_returns_none_if_undefined(self):
        """Check that the property returns None if undefined;
        Since this is the private method, it returns None
        """
        # Create a test instance of an ingredient with piece_mass undefined;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("piece_mass_undefined"))

        # Check the return value is None;
        self.assertIsNone(i._piece_mass_g)


# noinspection PyPep8Naming
class Test_CostPerQtyData(TestCase):
    """Tests the _cost_per_qty_data property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_data_if_defined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("cost_per_g_defined"))

        # Check the values are correct;
        self.assertEqual(0.002, i._cost_per_qty_data['cost_per_g'])
        self.assertEqual("g", i._cost_per_qty_data['pref_unit'])
        self.assertEqual(100, i._cost_per_qty_data['quantity_in_g'])

    @pfx.use_test_database
    def test_returns_correct_data_if_undefined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("cost_per_g_undefined"))

        # Check the values are correct;
        self.assertIsNone(i._cost_per_qty_data['cost_per_g'])
        self.assertEqual("g", i._cost_per_qty_data['pref_unit'])
        self.assertIsNone(i._cost_per_qty_data['quantity_in_g'])


# noinspection PyPep8Naming
class Test_FlagDOFs(TestCase):
    """Tests the _flag_dofs property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_data_if_defined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("flag_dofs_all_defined"))

        # Check the values are correct;
        self.assertTrue(i._flag_dofs['nut_free'])
        self.assertFalse(i._flag_dofs['vegan'])
        self.assertTrue(i._flag_dofs['vegetarian'])

    @pfx.use_test_database
    def test_returns_correct_data_if_undefined(self):
        """Checks we get the correct data back."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("flag_dofs_two_undefined"))

        # Check the values are correct;
        self.assertIsNone(i._flag_dofs['nut_free'])
        self.assertTrue(i._flag_dofs['vegan'])
        self.assertIsNone(i._flag_dofs['vegetarian'])


# noinspection PyPep8Naming
class Test_NutrientRatiosData(TestCase):
    """Tests the _nutrient_ratios_data property on the Ingredient class."""

    @pfx.use_test_database
    def test_returns_correct_data_for_defined_nutrient_ratios(self):
        """Checks we get the correct data back for defined nutrient ratios."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("nutrient_ratios_protein_defined"))

        # Check that there is a heading for protein;
        self.assertTrue("protein" in i._nutrient_ratios_data.keys())

        # Check the data is correct;
        self.assertEqual(0.1882, i._nutrient_ratios_data['protein']['nutrient_mass_data']['quantity_in_g'])
        self.assertEqual("g", i._nutrient_ratios_data['protein']['nutrient_mass_data']['pref_unit'])
        self.assertEqual(100, i._nutrient_ratios_data['protein']['subject_ref_qty_data']['quantity_in_g'])
        self.assertEqual("g", i._nutrient_ratios_data['protein']['subject_ref_qty_data']['pref_unit'])

    @pfx.use_test_database
    def test_excludes_undefined_nutrients(self):
        """Checks undefined nutrients do not show up in the nutrient data dict."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("nutrient_ratios_iron_undefined"))

        # Check that there is no heading for iron;
        self.assertFalse("iron" in i._nutrient_ratios_data.keys())

    @pfx.use_test_database
    def test_correct_number_nutrients_included(self):
        """Checks that the correct number of nutrients show up in the data dict."""
        # Create the test instance;
        i = model.ingredients.Ingredient(unique_name=fx.get_ingredient_name_with("nutrient_ratios_8_ratios_defined"))

        # Check that there is no heading for iron;
        self.assertEqual(8, len(i._nutrient_ratios_data))
