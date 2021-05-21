"""Test fixtures applicable to the entire testing module."""
from unittest import mock

import tests.configs


def use_test_database(func):
    """Patcher to point the model to the test database."""

    @mock.patch('persistence.configs.path_into_db', tests.configs.path_into_db)
    def wrapper(*args, **kwargs):
        """Wrapper function."""
        func(*args, **kwargs)

    return wrapper
