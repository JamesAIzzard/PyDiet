"""Tests for nutrients.main functions."""
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
