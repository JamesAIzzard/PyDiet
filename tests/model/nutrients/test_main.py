class TestGetNutrientPrimaryName(TestCase):
    @fx.use_test_nutrients
    def test_primary_name_is_returned_if_no_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('foo') == 'foo')

    @fx.use_test_nutrients
    def test_primary_name_is_returned_from_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('vibdo') == 'docbe')