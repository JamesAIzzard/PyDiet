from unittest import TestCase

import model


class TestAllFlags(TestCase):
    def test_flags_populated_during_init(self):
        self.assertTrue(len(model.flags.ALL_FLAGS) > 0)
