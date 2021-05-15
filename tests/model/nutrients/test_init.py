from unittest import TestCase

import model
import tests
from tests.model.nutrients import fixtures as fx


class TestBuildNutrientGroupNameList(TestCase):
    def test_builds_list_correctly(self):
        name_list = model.nutrients.build_nutrient_group_name_list(tests.model.nutrients.test_configs)
        self.assertEqual(len(name_list), 3)
        self.assertEqual(name_list, ["regatur", "docbe", "busskie"])


class TestPrimaryAndAliasNutrientNames(TestCase):
    @fx.use_test_nutrients
    def test_all_names_are_included_once(self):
        self.assertEqual(
            model.nutrients.PRIMARY_AND_ALIAS_NUTRIENT_NAMES,
            [
                "foo",
                "foobing",
                "bar",
                "gihumve",
                "fejaolka",
                "foobar",
                "docbe",
                "cufmagif",
                "bazing",
                "tirbur",
                "fillydon",
                "busskie",
                "regatur",
                "bingtong",
                "anatino", "vibdo", "sefling",
                "impstern", "golbuot", "terrnig"
            ]
        )


class TestGlobalNutrients(TestCase):
    @fx.use_test_nutrients
    def test_list_gets_populated_with_nutrients(self):
        # Check we have something in the global list;
        self.assertTrue(len(model.nutrients.GLOBAL_NUTRIENTS) ==
                        len(model.nutrients.configs.ALL_PRIMARY_NUTRIENT_NAMES))
        # Check those things are nutrients;
        self.assertTrue(isinstance(list(model.nutrients.GLOBAL_NUTRIENTS.values())[0], model.nutrients.Nutrient))


class TestNutrientGroupNames(TestCase):
    @fx.use_test_nutrients
    def test_all_group_names_are_included(self):
        self.assertTrue(len(model.nutrients.NUTRIENT_GROUP_NAMES)
                        == len(model.nutrients.configs.NUTRIENT_GROUP_DEFINITIONS))
        for group_name in model.nutrients.configs.NUTRIENT_GROUP_DEFINITIONS.keys():
            self.assertTrue(group_name in fx.NUTRIENT_GROUP_NAMES)


class TestOptionalNutrientNames(TestCase):
    @fx.use_test_nutrients
    def test_all_optional_names_are_present(self):
        self.assertEqual(
            set(model.nutrients.OPTIONAL_NUTRIENT_NAMES),
            {
                "foo",
                "foobing",
                "bar",
                "gihumve",
                "fejaolka",
                "foobar",
                "docbe",
                "bazing",
                "tirbur",
                "fillydon",
                "busskie"
            }
        )


class TestGetNutrientPrimaryName(TestCase):
    @fx.use_test_nutrients
    def test_primary_name_is_returned_if_no_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('foo') == 'foo')

    @fx.use_test_nutrients
    def test_primary_name_is_returned_from_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('vibdo') == 'docbe')
