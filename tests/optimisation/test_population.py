"""Tests for the Population class."""
from unittest import TestCase

import optimisation
import model


class TestPopulateWithRandomMembers(TestCase):
    """Tests the populate_with_random_members method."""

    def test_populates_correctly(self):
        """Checks the population is filled correctly."""

        # Create the population;
        pop = optimisation.Population(
            create_random_member=optimisation.create_random_member,
            calculate_fitness=optimisation.calculate_fitness,
            max_size=10
        )

        # Initialise;
        pop.populate_with_random_members()

        # Check the population members are the right type;
        for member in pop._population:
            self.assertTrue(isinstance(member, model.meals.SettableMeal))

        # Check there are the right number of objects in the population;
        self.assertEqual(10, len(pop))