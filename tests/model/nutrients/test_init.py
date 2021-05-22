"""Tests for the nutrient module initialisation functionality."""
from unittest import TestCase

import model
import tests


class TestBuildNutrientGroupNameList(TestCase):
    def test_builds_list_correctly(self):
        name_list = model.nutrients.build_nutrient_group_name_list(tests.model.nutrients.test_configs)
        self.assertEqual(len(name_list), 4)
        self.assertEqual(name_list, ["regatur", "docbe", "busskie", "fillydon"])


class TestBuildOptionalNutrientNameList(TestCase):
    def test_builds_list_correctly(self):
        name_list = model.nutrients.build_optional_nutrient_name_list(tests.model.nutrients.test_configs)
        self.assertEqual(len(name_list), 11)
        self.assertEqual(set(name_list), {
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
            "busskie",
        })


class TestBuildPrimaryAndAliasNutrientNames(TestCase):
    def test_builds_list_correctly(self):
        name_list = model.nutrients.build_primary_and_alias_nutrient_names(tests.model.nutrients.test_configs)
        self.assertEqual(len(name_list), 20)
        self.assertEqual(set(name_list), {
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
        })


class TestBuildGlobalNutrientList(TestCase):
    def test_list_contains_correct_instances(self):
        nutrient_list = model.nutrients.build_global_nutrient_list(tests.model.nutrients.test_configs)
        self.assertTrue(isinstance(list(nutrient_list.values())[0], model.nutrients.Nutrient))

    def test_builds_list_correctly(self):
        nutrient_list = model.nutrients.build_global_nutrient_list(tests.model.nutrients.test_configs)
        # Check we have the correct number;
        self.assertEqual(len(nutrient_list), 14)
        # Check we have the correct keys;
        self.assertEqual(
            set(nutrient_list.keys()),
            {
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
                "bingtong"
            }
        )


class TestGatherDescendants(TestCase):
    def test_gathers_descendants_correctly(self):
        self.assertEqual(
            set(model.nutrients._gather_descendant_names(
                primary_nutr_name="docbe",
                nutrient_configs=tests.model.nutrients.test_configs
            )),
            {"regatur", "bar", "tirbur", "cufmagif"},
        )


class TestGatherAscendants(TestCase):
    def test_gathers_ascendants_correctly(self):
        self.assertEqual(
            set(model.nutrients._gather_ascendant_names(
                primary_nutr_name="cufmagif",
                nutrient_configs=tests.model.nutrients.test_configs
            )),
            {"regatur", "docbe"}
        )


class TestGatherDirectSiblings(TestCase):
    def test_gathers_direct_siblings_correctly(self):
        self.assertEqual(
            set(model.nutrients._gather_direct_sibling_names(
                primary_nutr_name="cufmagif",
                nutrient_configs=tests.model.nutrients.test_configs
            )),
            {"tirbur"}
        )


class TestGatherDirectParentNames(TestCase):
    def test_gathers_direct_parent_names_correctly(self):
        self.assertEqual(
            set(model.nutrients._gather_direct_parent_names(
                primary_nutr_name="tirbur",
                nutrient_configs=tests.model.nutrients.test_configs
            )),
            {"regatur", "busskie"}
        )


class TestGatherDirectChildNames(TestCase):
    def test_gather_direct_child_names_correctly(self):
        self.assertEqual(
            set(model.nutrients._gather_direct_child_names(
                primary_nutr_name="regatur",
                nutrient_configs=tests.model.nutrients.test_configs
            )),
            {"tirbur", "cufmagif"}
        )


class TestGatherAllRelativeNames(TestCase):
    def test_gather_all_relative_names_correctly(self):
        self.assertEqual(
            set(model.nutrients._gather_all_relative_names(
                primary_nutr_name="regatur",
                nutrient_configs=tests.model.nutrients.test_configs
            )),
            {"docbe", "bar", "tirbur", "cufmagif", "busskie", "bingtong"}
        )
