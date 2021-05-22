"""Test fixtures to help with testing the persistence module."""
from unittest import mock

import tests


def use_test_database(func):
    """Decorator to apply all patches required to use the test database."""

    @mock.patch('persistence.configs.path_into_db', tests.persistence.configs.path_into_db)
    def wrapper(*args, **kwargs):
        """Wrapper function to return"""
        return func(*args, **kwargs)

    return wrapper
