"""Tests the HasIngredientQuantities class."""
# from unittest import TestCase
#
# import model
# from tests.persistence import fixtures as pfx
#
#
# class TestIngredientNames(TestCase):
#     """Tests the ingredient names property."""
#     @pfx.use_test_database
#     def test_correct_names_are_returned(self):
#         """Checks the method returns the correct list of names."""
#         # Create a test instance, with some ingredients;
#         hiq = fx.HasIngredientQuantitiesTestable(
#             ingredient_quantity_data=fx.get_ingredient_quantity_data()
#         )
#
#         # Assert the correct list of ingredient names are returned;
#         self.assertEqual({"Raspberry", "Aubergine", "Lemon Juice"}, set(hiq.ingredient_quantities))