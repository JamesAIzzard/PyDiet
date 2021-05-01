from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx
from tests.model.nutrients import nutrient_configs_for_testing


class TestConstructor(TestCase):
    def setUp(self) -> None:
        model.nutrients.configs = nutrient_configs_for_testing

    def test_can_be_instantiated(self) -> None:
        self.nutrient = model.nutrients.Nutrient("protein")
        self.assertTrue(isinstance(self.nutrient, model.nutrients.Nutrient))
        self.assertTrue(self.nutrient.primary_name == "protein")

    # While the following tests appear to be testing properties, the data the properties return is
    # initialised in the constructor, so they can be tested here;
    def test_contains_correct_direct_children(self) -> None:
        self.nutrient = model.nutrients.Nutrient("protein")
        # Check we have the correct number of children;
        self.assertTrue(
            len(self.nutrient.direct_child_nutrients) == 21
        )
        # Test some of the right nutrients are included in them;
        self.assertTrue(
            model.nutrients.GLOBAL_NUTRIENTS["valine"] in self.nutrient.direct_child_nutrients.values()
        )
        self.assertTrue(
            model.nutrients.GLOBAL_NUTRIENTS["gluten"] in self.nutrient.direct_child_nutrients.values()
        )

    def test_contains_correct_direct_parents(self) -> None:
        nutrient = model.nutrients.Nutrient("valine")
        self.assertTrue(
            len(nutrient.direct_parent_nutrients) == 1
        )
        self.assertTrue(
            model.nutrients.GLOBAL_NUTRIENTS["protein"] in nutrient.direct_parent_nutrients.values()
        )


class TestPrimaryName(TestCase):
    def test_primary_name_is_correct(self):
        self.assertTrue(fx.get_protein().primary_name == 'protein')

    def test_primary_name_is_correct_when_created_with_alias(self):
        self.assertTrue(fx.get_vitamin_b12().primary_name == 'cobalamin')
