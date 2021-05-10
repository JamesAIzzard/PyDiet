from unittest import TestCase, mock

import model
from tests.model.flags import fixtures as fx


class TestConstructor(TestCase):
    def test_correct_instance_is_created(self):
        hf = model.flags.HasSettableFlags()
        self.assertTrue(isinstance(hf, model.flags.HasSettableFlags))

    @fx.use_test_flags
    @mock.patch('model.flags.HasSettableFlags.load_data', mock.Mock())
    def test_calls_load_data_if_data_provided(self):
        flag_data = {
            "pongaterian": True,
            "foogetarian": True,
            "bar_free": False
        }
        hf = model.flags.HasSettableFlags(flag_data=flag_data)
        # noinspection PyUnresolvedReferences
        self.assertEqual(hf.load_data.call_args[0][0], {'flag_data': flag_data})

    @fx.use_test_flags
    @mock.patch('model.flags.HasSettableFlags.load_data', mock.Mock())
    def test_does_not_call_load_data_if_data_not_provided(self):
        hf = model.flags.HasSettableFlags()
        # noinspection PyUnresolvedReferences
        self.assertFalse(hf.load_data.called)


class TestFlagDOFS(TestCase):
    def test_returns_local_data(self):
        mock_data = mock.Mock()
        hf = model.flags.HasSettableFlags()
        hf._flag_dof_data = mock_data
        self.assertEqual(hf._flag_dofs, mock_data)


class TestCollectNutrientRatioConflicts(TestCase):
    """The following tests are based on the exhaustive list of scenarios listed in
    pydiet.docs.flag_conflict_logic_table.xlsx
    The test names here match test names in this table, and are ordered top to bottom.
    """

    def setUp(self):
        self.foo_free_no_conflicts = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.9),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4)  # Chuck another in just to mix things up.
        }
        self.foo_free_with_single_conflict = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4)  # Chuck another in just to mix things up.
        }
        self.foo_free_with_multiple_conflicts = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0.2),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.9),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0.1),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4)  # Chuck another in just to mix things up.
        }
        self.foo_free_with_undefined = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.9),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4)  # Chuck another in just to mix things up.
        }
        self.pongaterian_no_conflicts = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.2),
            "tirbur": fx.get_mock_nutrient_ratio("tirbur", 0.3)
        }
        self.pongaterian_with_conflicts = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.2),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0),
            "tirbur": fx.get_mock_nutrient_ratio("tirbur", 0.3)
        }
        self.pongaterian_with_undefined = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0),
            "tirbur": fx.get_mock_nutrient_ratio("tirbur", 0.3)
        }
        self.tirbur_free_no_conflicts = {
            "tirbur": fx.get_mock_nutrient_ratio("tirbur", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0),
        }

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_no_conflicts_when_changing_state_on_dof_with_no_nutrients(self):
        """Checks that, if we have no related nutrients at all, we are free to change from any state
        to any state."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foogetarian", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            conflicts = hf._collect_nutrient_ratio_conflicts("foogetarian", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            conflicts = hf._collect_nutrient_ratio_conflicts("foogetarian", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_no_conflicts_when_changing_state_on_dof_with_all_matching_nutrients(self):
        """This checks that an indirect alias with a set of related nutrients which match the flag, can be
        changed from any state to any state. If all related nutrients match the flag, the degree of freedom is free
        to change the flag from any value to any other value."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.pongaterian_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_true_to_true_returns_no_conflicts(self):
        """This checks that going from True to True (not changing the state) always returns no conflicts, with
        a DOF and direct alias flag type."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            # Check first with a direct alias;
            mock_nrs.return_value = self.foo_free_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", True)
            # Now check with a DOF flag;
            mock_nrs.return_value = self.pongaterian_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", True)
