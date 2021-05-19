# import model
# import tests
# from tests.model.ingredients import fixtures as fx
#
#
# class TestConstructor(tests.model.ingredients.UsesIngredientTestDB):
#
#     def test_correct_instance_is_returned(self):
#         iq = model.ingredients.SettableIngredientQuantity(ingredient=fx.get_honey())
#         self.assertTrue(isinstance(iq, model.ingredients.SettableIngredientQuantity))
#
#
# class TestIngredient(tests.model.ingredients.UsesIngredientTestDB):
#
#     def test_correct_ingredient_is_loaded(self):
#         hq = fx.get_undefined_honey_quantity()
#         self.assertTrue(hq.ingredient.name == "Honey")
