"""Tests for the optimisation.main module."""
from typing import Dict
from unittest import TestCase

import model
import optimisation
import persistence
from tests.optimisation import fixtures as ofx


class TestInitPopulation(TestCase):
    """Tests for the init_population method."""

    def setUp(self) -> None:
        persistence.cache.reset()

    def test_can_init_population(self):
        """Checks we can initialise a population."""
        # Create the population;
        pop = optimisation.init_population(
            num_members=10,
            create_member=lambda: optimisation.create_random_member(
                tags=['main', 'side', 'drink'],
                flags={
                    'vegetarian': True,
                    'nut_free': True
                }
            )
        )

        # Check the population members are the right type;
        for member in pop:
            self.assertTrue(isinstance(member, model.meals.SettableMeal))

        # Check there are the right number of objects in the population;
        self.assertEqual(10, len(pop))


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
            target_nutrient_masses=ofx.test_goals['target_nutrient_masses']
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
            target_nutrient_masses=ofx.test_goals['target_nutrient_masses']
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
            target_nutrient_masses=ofx.test_goals['target_nutrient_masses']
        )
        worse_fitness = optimisation.fitness_function(
            get_nutrient_ratio=lambda nutr_name: get_ratio(nutr_name, worse_member_ratios),
            target_nutrient_masses=ofx.test_goals['target_nutrient_masses']
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
