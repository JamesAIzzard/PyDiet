"""Tests for the HasSettableIngredientQuantities class."""
from unittest import TestCase

import model
from tests.model.ingredients import fixtures as ifx
from tests.model.quantity import fixtures as qfx
from tests.persistence import fixtures as pfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_simple_instance(self):
        """Checks we can construct a simple instance."""
        self.assertTrue(isinstance(model.ingredients.HasSettableIngredientQuantities(),
                                   model.ingredients.HasSettableIngredientQuantities))

    @pfx.use_test_database
    def test_supplied_data_is_loaded_correctly(self):
        """Checks that any data we pass in gets loaded correctly."""
        # Create some test data;
        iq_data = {
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        }

        # Create a test instance, passing this data in;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data=iq_data)

        # Check the data was passed in OK;
        self.assertEqual(iq_data, hsiq.persistable_data['ingredient_quantities_data'])


class TestIngredientQuantitiesData(TestCase):
    """Tests the ingredient_quantities_data property."""

    @pfx.use_test_database
    def test_correct_data_is_returned(self):
        """Check we get the correct data back from the property."""
        # Create some test data;
        iq_data = {
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        }

        # Create a test instance, passing this data in;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data=iq_data)

        # Check we get this data back;
        self.assertEqual(iq_data, hsiq.ingredient_quantities_data)


class TestIngredientQuantities(TestCase):
    """Tests the ingredient_quantities property."""

    @pfx.use_test_database
    def test_correct_instance_type_is_returned(self):
        """Check that we get ReadonlyIngredientQuantity instances back."""
        # Create a test instance, passing this data in;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Check that each instance is a ReadonlyIngredientQuantity;
        for iq in hsiq.ingredient_quantities.values():
            self.assertTrue(isinstance(iq, model.ingredients.SettableIngredientQuantity))

    @pfx.use_test_database
    def test_correct_number_of_results_returned(self):
        """Checks that we get the right number of results back from the method."""
        # Create a test instance, passing this data in;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Assert there are the right number of results;
        self.assertEqual(3, len(hsiq.ingredient_quantities))

    @pfx.use_test_database
    def test_instances_have_correct_data(self):
        """Checks that the ReadonlyIngredientQuantity instances which get returned are loaded with
        the correct data."""
        # Create a test instance, with some ingredients;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Grab the return values from the method;
        iqs = hsiq.ingredient_quantities

        # Check that we have the correct quantities of each ingredient;
        self.assertEqual(100, iqs[ifx.get_ingredient_df_name("Raspberry")].quantity_in_g)
        self.assertEqual(110, iqs[ifx.get_ingredient_df_name("Aubergine")].quantity_in_g)
        self.assertEqual(120, iqs[ifx.get_ingredient_df_name("Lemon Juice")].quantity_in_g)

    @pfx.use_test_database
    def test_can_set_an_ingredient_quantity(self):
        """Checks we can set an ingredient quantity."""
        # Create a test instance, with some ingredients;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        })

        # Grab the return values from the method;
        iqs = hsiq.ingredient_quantities

        # Check the quantity of an ingredient prior to change;
        self.assertEqual(100, iqs[ifx.get_ingredient_df_name("Raspberry")].quantity_in_g)

        # Now change it;
        iqs[ifx.get_ingredient_df_name("Raspberry")].set_quantity(quantity_value=0.5, quantity_unit='kg')

        # Assert the change is reflected in the data;
        self.assertEqual(
            500,
            hsiq.ingredient_quantities_data[ifx.get_ingredient_df_name("Raspberry")]['quantity_in_g']
        )

    @pfx.use_test_database
    def test_exception_when_setting_ingredient_qty_in_vol_and_ingredient_density_not_configured(self):
        """Checks we get an exception if we set an ingredient quantity using volumentric units, and
        the density is not configured on that ingredient."""
        # Grab an ingredient name with density not configured;
        ndiun = ifx.get_ingredient_name_with("density_undefined")  # no-density-ingredient-unique-name
        ndidfn = ifx.get_ingredient_df_name(unique_name=ndiun)  # no-density-ingredient-df-name

        # Create a test instance, passing in the ingredient without density;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ndidfn: qfx.get_qty_data(qty_in_g=120),
        })

        # Check we get an exception if we try to set the no-density ingredient qty using volumes;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            hsiq.ingredient_quantities[ndidfn].set_quantity(quantity_value=1.1, quantity_unit="L")

    @pfx.use_test_database
    def test_no_exception_when_setting_ingredient_qty_in_vol_and_density_configured(self):
        """Checks we don't get an exception if we set an ingredient quantity using volumetric units, and
        the ingredient has density configured."""
        # Grab an ingredient with density configured;
        iunwd = ifx.get_ingredient_name_with("density_defined")  # ingredient-unique-name-with-density
        idfnwd = ifx.get_ingredient_df_name(unique_name=iunwd)  # ingredient-df-name-with-density

        # Create a test instance, passing in the ingredient with density;
        hsiq = model.ingredients.HasSettableIngredientQuantities(ingredient_quantities_data={
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            idfnwd: qfx.get_qty_data(qty_in_g=120),
        })

        # Check we can set the ingredient qty with density units;
        hsiq.ingredient_quantities[idfnwd].set_quantity(quantity_value=250, quantity_unit="ml")


class TestAddIngredientQuantity(TestCase):
    """Tests the add_ingredient_quantity method."""

    @pfx.use_test_database
    def test_can_add_ingredient_quantity(self):
        """Tests we can add an ingredient quantity without exception."""
        # Create an empty test instance;
        hsiq = model.ingredients.HasSettableIngredientQuantities()

        # Assert there are no ingredient quantites yet;
        self.assertEqual(0, len(hsiq.ingredient_quantities))

        # Add an ingredient quantity;
        i_uq_name = ifx.get_ingredient_name_with("typical_fully_defined_data")
        i_df_name = ifx.get_ingredient_df_name(i_uq_name)
        hsiq.add_ingredient_quantity(
            ingredient_unique_name=i_uq_name,
            qty_value=100,
            qty_unit='g'
        )

        # Assert there is now an ingredient quantity;
        self.assertEqual(1, len(hsiq.ingredient_quantities))

        # Assert it has the right quantity;
        self.assertEqual(100, hsiq.ingredient_quantities[i_df_name].quantity_in_g)

    @pfx.use_test_database
    def test_exception_if_adding_with_vol_unit_when_density_not_configured(self):
        """Check we get an exception if we try to add an ingredient in vol units if vol not configured."""
        # Create an empty test instance;
        hsiq = model.ingredients.HasSettableIngredientQuantities()

        # Assert we get an exception if we try and add a volume of an ingredient without density configured;
        with self.assertRaises(model.quantity.exceptions.UndefinedDensityError):
            hsiq.add_ingredient_quantity(
                ingredient_unique_name=ifx.get_ingredient_name_with("density_undefined"),
                qty_value=1.5,
                qty_unit="L"
            )

    @pfx.use_test_database
    def test_no_exception_if_adding_with_vol_unit_when_density_configured(self):
        """Check we can add a volume of an ingredient with density configured."""
        # Create an empty test instance;
        hsiq = model.ingredients.HasSettableIngredientQuantities()

        # Grab the names for an ingredient with known density;
        uqn = ifx.get_ingredient_name_with("1.2g_per_ml")
        dfn = ifx.get_ingredient_df_name(unique_name=uqn)

        # Assert we can add a volume of an ingredient with density configured;
        hsiq.add_ingredient_quantity(
            ingredient_unique_name=uqn,
            qty_value=1.5,
            qty_unit="L"
        )

        # Assert the qty_in_g is correct;
        self.assertEqual(1.2 * 1500, hsiq.ingredient_quantities[dfn].quantity_in_g)


class TestLoadData(TestCase):
    """Tests the load_data method."""

    @pfx.use_test_database
    def test_data_is_loaded_correctly(self):
        """Checks that the method loads data onto the instance correctly."""
        # Create a blank instance;
        hsiq = model.ingredients.HasSettableIngredientQuantities()

        # Assert there are no ingredient quantities;
        self.assertEqual(0, len(hsiq.ingredient_quantities))

        # Load the data;
        data = {
            ifx.get_ingredient_df_name("Raspberry"): qfx.get_qty_data(qty_in_g=100),
            ifx.get_ingredient_df_name("Aubergine"): qfx.get_qty_data(qty_in_g=110),
            ifx.get_ingredient_df_name("Lemon Juice"): qfx.get_qty_data(qty_in_g=120),
        }
        hsiq.load_data({'ingredient_quantities_data': data})

        # Assert there are now three ingredient quantities;
        self.assertEqual(3, len(hsiq.ingredient_quantities))

        # Check some of the values;
        self.assertEqual(100, hsiq.ingredient_quantities[ifx.get_ingredient_df_name("Raspberry")].quantity_in_g)
        self.assertEqual(110, hsiq.ingredient_quantities[ifx.get_ingredient_df_name("Aubergine")].quantity_in_g)
        self.assertEqual(120, hsiq.ingredient_quantities[ifx.get_ingredient_df_name("Lemon Juice")].quantity_in_g)
