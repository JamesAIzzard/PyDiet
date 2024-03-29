"""Test fixtures to help with testing the persistence module."""
from unittest import mock

import tests
import persistence


def use_test_database(func):
    """Decorator to apply all patches required to use the test database."""

    @mock.patch('persistence.configs.PATH_INTO_DB', tests.persistence.configs.PATH_INTO_DB)
    def wrapper(*args, **kwargs):
        """Wrapper function to return"""
        persistence.cache.reset()
        return func(*args, **kwargs)

    return wrapper
