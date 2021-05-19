# from unittest import TestCase
#
# import model
# import persistence
# import tests
# from tests.model.ingredients import fixtures as fx
#
#
# class TestConstructor(TestCase):
#     def test_returns_correct_instance(self):
#         i = model.ingredients.Ingredient()
#         self.assertTrue(isinstance(i, model.ingredients.Ingredient))
#
#
# class TestUniqueValue(tests.model.ingredients.UsesIngredientTestDB):
#     def test_gets_unique_value_correctly(self):
#         self.assertTrue(fx.get_honey().unique_value == "Honey")
#
#     def test_exception_when_setting_duplicated_unique_value(self):
#         honey: 'model.HasSettableName' = fx.get_honey()
#         with self.assertRaises(persistence.exceptions.UniqueValueDuplicatedError):
#             honey.name = "Cucumber"
#
#     def test_sets_unique_value_correctly(self):
#         honey = fx.get_honey()
#         honey.name = "Runny Honey"
#         self.assertTrue(honey.unique_value == "Runny Honey")
