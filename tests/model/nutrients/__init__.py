"""Initialisation for nutrients testing module."""
import model
from . import fixtures, test_configs

# Validate the test configs;
model.nutrients.main.validate_configs(test_configs)
