# from unittest import TestCase
#
# from model import recipes
#
#
# class TestConstructor(TestCase):
#
#     def test_creates_fresh_recipe_instance(self) -> None:
#         r = recipes.Recipe()
#         self.assertTrue(isinstance(r, recipes.Recipe))
#
#
# class TestName(TestCase):
#     def setUp(self) -> None:
#         self.recipe = recipes.Recipe()
#
#     def test_name_sets_and_gets_correctly(self) -> None:
#         self.assertEqual(self.recipe.name, None)
#         self.recipe.name = "Orange Juice"
#         self.assertEqual(self.recipe.name, "Orange Juice")
#
#
# class TestAddIngredientRatio(TestCase):
#     def test_ingredient_ratio_is_added(self):
#         self.recipe = recipes.Recipe()
#         self.recipe.add_ingredient_ratio(
#             ingredient_name="Cucumber",
#             ingredient_nominal_quantity=100,
#             ingredient_nominal_quantity_units='g',
#             inc_perc=5,
#             dec_perc=10
#         )
#         self.assertTrue("0c5e02cc-97ba-41a0-aa27-db8517a33cf3" in self.recipe._ingredient_ratios.keys())
#         ir = self.recipe._ingredient_ratios["0c5e02cc-97ba-41a0-aa27-db8517a33cf3"]
#         self.assertEqual(ir.ingredient_name, "Cucumber")
#         self.assertEqual(ir.quantity_in_g, 100)
#         self.assertEqual(ir.quantity_pref_units, 'g')
#         self.assertEqual(ir.perc_incr, 5)
#         self.assertEqual(ir.perc_decr, 10)
#
#
# class TestGetIngredientRatio(TestCase):
#     def setUp(self):
#         self.recipe = recipes.Recipe()
#         self.recipe.add_ingredient_ratio(
#             ingredient_name="Cucumber",
#             ingredient_nominal_quantity=100,
#             ingredient_nominal_quantity_units='g',
#             inc_perc=5,
#             dec_perc=10
#         )
#
#     def test_ingredient_ratio_can_be_retrieved_by_ingredient_name(self) -> None:
#         ir = self.recipe.get_ingredient_ratio(
#             ingredient_name="Cucumber"
#         )
#         self.assertTrue(isinstance(ir, recipes.RecipeIngredientRatio))
#         self.assertTrue(ir.ingredient_name, "Cucumber")
#
#
# class TestDeleteIngredientRatio(TestCase):
#     def setUp(self):
#         self.recipe = recipes.Recipe()
#         self.recipe.add_ingredient_ratio(
#             ingredient_name="Cucumber",
#             ingredient_nominal_quantity=100,
#             ingredient_nominal_quantity_units='g',
#             inc_perc=5,
#             dec_perc=10
#         )
#
#     def test_ingredient_ratio_can_be_deleted(self) -> None:
#         self.assertTrue("0c5e02cc-97ba-41a0-aa27-db8517a33cf3" in self.recipe._ingredient_ratios.keys())
#         self.recipe.delete_ingredient_ratio(
#             ingredient_name="Cucumber"
#         )
#         self.assertTrue("0c5e02cc-97ba-41a0-aa27-db8517a33cf3" not in self.recipe._ingredient_ratios.keys())
