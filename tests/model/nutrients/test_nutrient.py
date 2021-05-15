from unittest import TestCase

from tests.model.nutrients import fixtures as fx


class TestPrimaryName(TestCase):
    def test_primary_name_is_correct(self):
        self.assertEqual("docbe", fx.GLOBAL_NUTRIENTS["docbe"].primary_name)


class TestDirectChildNutrients(TestCase):
    def test_child_nutrients_are_correct(self):
        self.assertEqual({
            fx.GLOBAL_NUTRIENTS["tirbur"],
            fx.GLOBAL_NUTRIENTS["cufmagif"]
        }, set(fx.GLOBAL_NUTRIENTS["regatur"].direct_child_nutrients.values()))


class TestDirectParentNutrients(TestCase):
    def test_parent_nutrients_are_correct(self):
        self.assertEqual({
            fx.GLOBAL_NUTRIENTS["regatur"],
            fx.GLOBAL_NUTRIENTS["busskie"]
        }, set(fx.GLOBAL_NUTRIENTS["tirbur"].direct_parent_nutrients.values()))


class TestAllSiblingNutrients(TestCase):
    def test_sibling_nutrients_are_correct(self):
        self.assertEqual({
            fx.GLOBAL_NUTRIENTS["bazing"],
            fx.GLOBAL_NUTRIENTS["fejaolka"]
        }, set(fx.GLOBAL_NUTRIENTS["foo"].all_sibling_nutrients.values()))


class TestAllAscendantNutrients(TestCase):
    def test_ascendant_nutrients_are_correct(self):
        self.assertEqual({
            fx.GLOBAL_NUTRIENTS["regatur"],
            fx.GLOBAL_NUTRIENTS["docbe"],
            fx.GLOBAL_NUTRIENTS["busskie"]
        }, set(fx.GLOBAL_NUTRIENTS["tirbur"].all_ascendant_nutrients.values()))


class TestAllDescendantNutrients(TestCase):
    def test_descendant_nutrients_are_correct(self):
        self.assertEqual({
            fx.GLOBAL_NUTRIENTS["tirbur"],
            fx.GLOBAL_NUTRIENTS["bar"],
            fx.GLOBAL_NUTRIENTS["regatur"],
            fx.GLOBAL_NUTRIENTS["cufmagif"]
        }, set(fx.GLOBAL_NUTRIENTS["docbe"].all_descendant_nutrients.values()))


class TestAllRelativeNutrients(TestCase):
    def test_relative_nutrients_are_correct(self):
        self.assertEqual({
            fx.GLOBAL_NUTRIENTS["regatur"],
            fx.GLOBAL_NUTRIENTS["docbe"],
            fx.GLOBAL_NUTRIENTS["tirbur"],
            fx.GLOBAL_NUTRIENTS["cufmagif"],
            fx.GLOBAL_NUTRIENTS["bingtong"],
            fx.GLOBAL_NUTRIENTS["busskie"]
        }, set(fx.GLOBAL_NUTRIENTS["bar"].all_relative_nutrients.values()))


class TestAliasNames(TestCase):
    def test_alias_names_returned_correctly(self):
        self.assertEqual({"anatino", "vibdo", "sefling"}, set(fx.GLOBAL_NUTRIENTS["docbe"].alias_names))

    def test_returns_empty_if_no_alias(self):
        self.assertEqual([], fx.GLOBAL_NUTRIENTS["foo"].alias_names)


class TestCaloriesPerG(TestCase):
    def test_cals_returned_correctly_when_present(self):
        self.assertEqual(3, fx.GLOBAL_NUTRIENTS["regatur"].calories_per_g)

    def test_returns_zero_when_no_cals_per_g(self):
        self.assertEqual(0, fx.GLOBAL_NUTRIENTS["tirbur"].calories_per_g)
