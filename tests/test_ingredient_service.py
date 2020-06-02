from unittest import TestCase

from pydiet.ingredients import ingredient_service as igs

class TestGetMatchingNutrientNames(TestCase):
    def test_returns_matching_names(self):
        search_term = "protein"
        results = igs.get_matching_nutrient_names(search_term, 4)
        self.assertEqual(results[0], 'protein')

class TestSummariseDensity(TestCase):
    def setUp(self):
        self.i = igs.load_new_ingredient()
    
    def test_returns_undefined(self):
        # Check the density is undefined to start with;
        self.assertEqual(igs.summarise_density(self.i), 'Undefined')
        # Set the density;
        self.i.set_density(1, 'L', 1, 'kg')
        # Check the summary now appears;
        print(igs.summarise_density(self.i))
        pass