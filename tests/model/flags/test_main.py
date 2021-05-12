from unittest import TestCase

import model
from . import fixtures as fx


class TestAllFlags(TestCase):

    @fx.use_test_flags
    def test_flags_populated_during_init(self):
        self.assertTrue(len(model.flags.ALL_FLAGS) == 5)
