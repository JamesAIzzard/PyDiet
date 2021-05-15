from typing import Dict
from unittest import TestCase

import model
from tests.model.nutrients import fixtures as fx


class TestGetNutrientPrimaryName(TestCase):
    @fx.use_test_nutrients
    def test_primary_name_is_returned_if_no_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('foo') == 'foo')

    @fx.use_test_nutrients
    def test_primary_name_is_returned_from_alias(self):
        self.assertTrue(model.nutrients.get_nutrient_primary_name('vibdo') == 'docbe')

    @fx.use_test_nutrients
    def test_raises_exception_if_name_not_recognised(self):
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            _ = model.nutrients.get_nutrient_primary_name("fake")


class TestGetNutrientAliasNames(TestCase):
    @fx.use_test_nutrients
    def test_returns_correct_alias_names(self):
        self.assertEqual(
            set(model.nutrients.get_nutrient_alias_names("docbe")),
            {"anatino", "vibdo", "sefling"}
        )

    @fx.use_test_nutrients
    def test_raises_exception_if_name_not_recognised(self):
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            _ = model.nutrients.get_nutrient_alias_names("fake")


class TestGetCaloriesPerG(TestCase):
    @fx.use_test_nutrients
    def test_returns_correct_value_if_nutrient_has_cals(self):
        self.assertEqual(1, model.nutrients.get_calories_per_g("fillydon"))

    @fx.use_test_nutrients
    def test_returns_zero_if_nutrient_has_no_cals(self):
        self.assertEqual(0, model.nutrients.get_calories_per_g("docbe"))

    @fx.use_test_nutrients
    def test_raises_exception_if_name_not_recognised(self):
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            _ = model.nutrients.get_calories_per_g("fake")


class TestValidateNutrientFamilyMasses(TestCase):
    def setUp(self):
        self.nutrient_masses: Dict[str, float] = {}

        def _get_nutrient_mass_g(nutrient_name: str) -> float:
            try:
                return self.nutrient_masses[nutrient_name]
            except KeyError:
                raise model.nutrients.exceptions.UndefinedNutrientMassError()

        self.get_nutrient_mass_g = _get_nutrient_mass_g

    @fx.use_test_nutrients
    def test_no_exception_if_no_error(self):
        self.nutrient_masses = {
            "regatur": 10,
            "docbe": 12,
            "tirbur": 4
        }
        model.nutrients.validate_nutrient_family_masses("tirbur", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_child_exceeds_parent(self):
        self.nutrient_masses = {
            "regatur": 20,
            "docbe": 12,
            "tirbur": 14
        }
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validate_nutrient_family_masses("tirbur", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_child_exceeds_parent_2(self):
        self.nutrient_masses = {
            "foo": 20,
            "docbe": 12,
            "tirbur": 14,
            "fillydon": 18
        }
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validate_nutrient_family_masses("foo", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_grandchild_exceeds_parent(self):
        self.nutrient_masses = {
            "cufmagif": 20,
            "docbe": 12
        }
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validate_nutrient_family_masses("tirbur", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_grandchild_exceeds_parent_2(self):
        self.nutrient_masses = {
            "tirbur": 20,
            "docbe": 12
        }
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validate_nutrient_family_masses("docbe", self.get_nutrient_mass_g)
