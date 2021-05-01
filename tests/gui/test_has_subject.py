# from unittest import TestCase
# import tkinter as tk
#
# import model
# import gui


# class TestSubjectSetter(TestCase):
#     def setUp(self) -> None:
#         root = tk.Tk()
#         view = gui.IngredientEditorView(master=root)
#         self.ctrl = gui.IngredientEditorController(view=view)
#
#     def test_raises_exception_if_wrong_subject_type_is_passed(self) -> None:
#         with self.assertRaises(TypeError):
#             self.ctrl.set_subject(object()) # noqa
#
#     def test_sets_correct_type_ok(self) -> None:
#         self.ctrl.set_subject(model.ingredients.Ingredient())
