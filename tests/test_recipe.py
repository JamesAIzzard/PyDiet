from unittest import TestCase

from pydiet.recipes import recipe_service

class TestStepTools(TestCase):

    def setUp(self):
        self.recipe = recipe_service.load_new_recipe()
        self.step1 = 'This is the first step.'
        self.step2 = 'This is the second step.'
        self.step3 = 'This is the third step.'
        self.recipe.append_step(self.step1)
        self.recipe.append_step(self.step2)
        self.recipe.append_step(self.step3)        

    def test_steps_added(self):
        self.assertEqual(self.recipe.steps[1], self.step1)
        self.assertEqual(self.recipe.steps[2], self.step2)
        self.assertEqual(self.recipe.steps[3], self.step3)

    def test_remove_step(self):
        self.recipe.remove_step(2)
        self.assertEqual(self.recipe.steps[1], self.step1)
        self.assertEqual(self.recipe.steps[2], self.step3)
        self.assertEqual(len(self.recipe.steps), 2)
        self.setUp()
        self.recipe.remove_step(1)
        self.assertEqual(self.recipe.steps[1], self.step2)
        self.assertEqual(self.recipe.steps[2], self.step3)
        self.assertEqual(len(self.recipe.steps), 2)
        self.setUp()
        self.recipe.remove_step(3)
        self.recipe.remove_step(1)
        self.assertEqual(self.recipe.steps[1], self.step2)
        self.assertEqual(len(self.recipe.steps), 1)

    def test_move_step(self):
        self.recipe.move_step(1, 3)
        self.assertEqual(self.recipe.steps[1], self.step2)
        self.assertEqual(self.recipe.steps[2], self.step3)
        self.assertEqual(self.recipe.steps[3], self.step1) 
        self.setUp()
        self.recipe.move_step(2, 1)
        self.assertEqual(self.recipe.steps[1], self.step2)
        self.assertEqual(self.recipe.steps[2], self.step1)
        self.assertEqual(self.recipe.steps[3], self.step3)
        self.setUp()
        self.recipe.move_step(1, 3)
        self.assertEqual(self.recipe.steps[1], self.step2)
        self.assertEqual(self.recipe.steps[2], self.step3)
        self.assertEqual(self.recipe.steps[3], self.step1)          