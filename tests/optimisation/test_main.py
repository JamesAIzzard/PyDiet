"""Tests for the optimisation.main module."""
from typing import Dict
from unittest import TestCase

import optimisation
import persistence
from tests.optimisation import fixtures as ofx


class TestInitPopulation(TestCase):
    """Tests for the init_population method."""

    def setUp(self) -> None:
        persistence.cache.reset()


class TestFitnessFunction(TestCase):
    """Tests for the fitness_function mehtod."""

    def setUp(self):
        persistence.cache.reset()

    def test_returns_one_for_perfect_solution(self):
        """Check that the fitness function returns a float."""
        # Create a set of test ratios, and a method to fetch them by name;
        member_ratios = {
            "protein": 0.3,
            "carbohydrate": 0.4,
            "fat": 0.3
        }

        def get_ratio(nutr_name: str) -> float:
            return member_ratios[nutr_name]

        # Assert that the fitness function returns a float;
        self.assertEqual(1, optimisation.fitness_function(
            get_nutrient_ratio=get_ratio,
            target_nutrient_ratios=ofx.test_goals['target_nutrient_ratios']
        ))

    def test_returns_less_than_one_for_imperfect_solution(self):
        """Check that the fitness function returns less than one for an imperfect solution."""
        # Create a set of test ratios, and a method to fetch them by name;
        member_ratios = {
            "protein": 0.0,
            "carbohydrate": 0.5,
            "fat": 0.3
        }

        def get_ratio(nutr_name: str) -> float:
            return member_ratios[nutr_name]

        # Assert that the fitness function returns a float;
        self.assertLess(optimisation.fitness_function(
            get_nutrient_ratio=get_ratio,
            target_nutrient_ratios=ofx.test_goals['target_nutrient_ratios']
        ), 1)

    def test_better_solution_scores_higher_than_worse_solution(self):
        """Checks that a better solution scores higher than a worse solution."""
        # Create a set of test ratios, and a method to fetch them by name;
        better_member_ratios = {
            "protein": 0.2,
            "carbohydrate": 0.5,
            "fat": 0.3
        }

        worse_member_ratios = {
            "protein": 0.1,
            "carbohydrate": 0.5,
            "fat": 0.4
        }

        def get_ratio(nutr_name: str, ratios: Dict[str, float]) -> float:
            return ratios[nutr_name]

        # Calc results for better and worse ratios;
        better_fitness = optimisation.fitness_function(
            get_nutrient_ratio=lambda nutr_name: get_ratio(nutr_name, better_member_ratios),
            target_nutrient_ratios=ofx.test_goals['target_nutrient_ratios']
        )
        worse_fitness = optimisation.fitness_function(
            get_nutrient_ratio=lambda nutr_name: get_ratio(nutr_name, worse_member_ratios),
            target_nutrient_ratios=ofx.test_goals['target_nutrient_ratios']
        )

        # Assert that the fitness function returns a float;
        self.assertLess(worse_fitness, better_fitness)


class TestMutateMember(TestCase):
    """Tests the mutate_member function."""

    def test_changes_member_quantity(self):
        """Makes sure the member quantity gets changed;"""
        # Create a test member;
        m = optimisation.create_random_member(
            tags=["main", "side", "drink"],
            flags={
                "vegetarian": True,
                "nut_free": True
            }
        )

        # Log the quantities before;
        qts_before = {}
        for rdfn, rqty in m.recipe_quantities.items():
            qts_before[rdfn] = rqty.quantity_in_g

        # Mutate;
        optimisation.mutate_member(m)

        # Log quantities after;
        qts_after = {}
        for rdfn, rqty in m.recipe_quantities.items():
            qts_after[rdfn] = rqty.quantity_in_g

        # Assert the recipe qty dict has changed;
        changed = False
        for rdf in qts_after:
            if not qts_before[rdf] == qts_after[rdf]:
                changed = True
        self.assertTrue(changed)


class TestSpliceMembers(TestCase):
    """Tests the splice members function."""

    def test_recipe_quantities_come_from_parents(self):
        """Checks that the recipe quantities in the child have come from the parents."""
        # Inputs to create test member;
        tags = ["main", "side", "drink"]
        flags = {
            "vegetarian": True,
            "nut_free": True
        }

        # Create a couple of test members;
        m1 = optimisation.create_random_member(tags=tags, flags=flags)
        m2 = optimisation.create_random_member(tags=tags, flags=flags)

        # Group their recipe qts by tag;
        tags = {}
        for rq in list(m1.recipe_quantities.values())+list(m2.recipe_quantities.values()):
            if rq.recipe.tags[0] not in tags:
                tags[rq.recipe.tags[0]] = []
            tags[rq.recipe.tags[0]].append(rq.quantity_in_g)

        m3 = optimisation.splice_members(m1, m2)
        for rq in m3.recipe_quantities.values():
            self.assertTrue(rq.quantity_in_g in tags[rq.recipe.tags[0]])
