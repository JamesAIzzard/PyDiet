from unittest import TestCase

import model
import gui


class TestSubjectSetter(TestCase):
    def setUp(self) -> None:
        self.hs = gui.HasSubject(subject_type=model.ingredients.Ingredient)

    def test_raises_exception_if_wrong_subject_type_is_passed(self) -> None:
        with self.assertRaises(TypeError):
            self.hs.subject = object()

    def test_sets_correct_type_ok(self) -> None:
        self.hs.subject = model.ingredients.Ingredient()
