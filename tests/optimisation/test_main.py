"""Tests for the optimisation.main module."""
from unittest import TestCase

import model
import optimisation


class TestInitPopulation(TestCase):
    """Tests for the init_population method."""

    def test_can_init_population(self):
        """Checks we can initialise a population."""
        # Create the population;
        pop = optimisation.init_population(
            num_members=1000,
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
        self.assertEqual(1000, len(pop))
