"""Tests for the nutrient validation methods."""
from unittest import TestCase
from typing import Dict

import model
from tests.model.nutrients import fixtures as fx


class TestValidateNutrientFamilyMasses(TestCase):
    """Tests for validate_nutrient_family_masses."""
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
        """Checks we get no exception if the nutrient masses do not conflict;"""
        # Create some test masses;
        self.nutrient_masses = {
            "regatur": 10,
            "cufmagif": 6,
            "docbe": 12,
            "tirbur": 4,
            "bar": 2
        }

        # Run the validation to ensure no error is raised;
        model.nutrients.validation.validate_nutrient_family_masses("tirbur", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_child_exceeds_parent(self):
        """Checks we get an exception if a child mass exceeds a parent group mass."""
        # Create a set of nutrient masses, in which a child mass exceeds a parent group mass;
        self.nutrient_masses = {
            "regatur": 20,
            "docbe": 12,
            "tirbur": 14
        }

        # Assert the correct exception is raised when we run validation;
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validation.validate_nutrient_family_masses("tirbur", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_child_exceeds_parent_2(self):
        """Checks we get an exception on anther variation of a child mass exceeding a parent group mass."""
        # Create a set of nutrient masses;
        self.nutrient_masses = {
            "foo": 20,
            "docbe": 12,
            "tirbur": 14,
            "fillydon": 18
        }

        # Assert the correct exception is raised when we run validation;
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validation.validate_nutrient_family_masses("foo", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_grandchild_exceeds_parent(self):
        """Checks that we get an exception if the grandchild exceeds a parent mass."""
        self.nutrient_masses = {
            "cufmagif": 20,
            "docbe": 12
        }

        # Assert that the correct exception is raised when we run validation'
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validation.validate_nutrient_family_masses("tirbur", self.get_nutrient_mass_g)

    @fx.use_test_nutrients
    def test_raises_exception_if_grandchild_exceeds_parent_2(self):
        """Checks that we get an exception if the grandchild exceeds a parent mass."""
        self.nutrient_masses = {
            "tirbur": 20,
            "docbe": 12
        }

        # Assert that the correct exception is raised if we run validation;
        with self.assertRaises(model.nutrients.exceptions.ChildNutrientExceedsParentMassError):
            model.nutrients.validation.validate_nutrient_family_masses("docbe", self.get_nutrient_mass_g)


class TestValidateNutrientName(TestCase):
    """Tests the validate_nutrient_name method."""

    @fx.use_test_nutrients
    def test_returns_primary_name(self):
        """Check that the a primary name is returned if it is valid."""
        # Assert we get a valid primary name back;
        self.assertEqual("foo", model.nutrients.validation.validate_nutrient_name("foo"))

    @fx.use_test_nutrients
    def test_returns_alias_name(self):
        """Check that the a alias name is returned if it is valid."""
        # Assert we get a valid alias name back;
        self.assertEqual("anatino", model.nutrients.validation.validate_nutrient_name("anatino"))

    @fx.use_test_nutrients
    def test_raises_exception_if_name_not_recognised(self):
        """Check that we get an exception if the name is not recognised."""
        with self.assertRaises(model.nutrients.exceptions.NutrientNameNotRecognisedError):
            _ = model.nutrients.validation.validate_nutrient_name("fake")
