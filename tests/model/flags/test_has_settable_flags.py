from unittest import TestCase, mock
from unittest.mock import call

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


# noinspection DuplicatedCode
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
        self.foo_free_multiple_undefined = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
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
        self.pongaterian_with_multiple_undefined = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
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

        self.bar_free_no_conflicts = {
            "bar": fx.get_mock_nutrient_ratio("bar", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0.2),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0),
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
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            # Now check with a DOF flag;
            mock_nrs.return_value = self.pongaterian_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_false_to_false_returns_no_conflicts(self):
        """This checks that going from False to False (not changing the state) always returns no conflicts, with
        a DOF and direct alias flag type."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            # Check first with a direct alias;
            mock_nrs.return_value = self.foo_free_with_multiple_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            # Now check with a DOF flag;
            mock_nrs.return_value = self.pongaterian_with_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_none_to_none_returns_no_conflicts(self):
        """This checks that going from None to None (not changing the state) always returns no conflicts, with
        a DOF and direct alias flag type."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            # Check first with a direct alias;
            mock_nrs.return_value = self.foo_free_with_undefined
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)
            # Now check with a DOF flag;
            mock_nrs.return_value = self.pongaterian_with_undefined
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_none_to_true_correctly_categorises_nutrients(self):
        """This checks that going from None to True correctly collects related
        nutrients into need_zero and need_non_zero to match their implications."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            # Check first with a direct alias;
            mock_nrs.return_value = self.foo_free_with_undefined
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_zero": ["foobar"]}
            ), conflicts)
            # Now check with a DOF flag;
            mock_nrs.return_value = self.pongaterian_with_undefined
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_non_zero": ["bazing"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_false_to_true_correctly_categorises_nutrients(self):
        """This checks that going from False to True correctly collects related
        nutrients into need_zero and need_non_zero to match their implications."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            # Check first with a direct alias;
            mock_nrs.return_value = self.foo_free_with_multiple_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_zero": ["foo", "foobar"]}
            ), conflicts)
            # Now check with a DOF flag;
            mock_nrs.return_value = self.pongaterian_with_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", True)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_zero": ["foobing"], "need_non_zero": ["bazing"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_true_to_false_with_direct_alias_single_nutrient_correctly_categorises_opposing_implication(self):
        """This checks that going from True to False with a single nutrient correctly collects related
        nutrient in the group opposing its implication. We only do this check with a direct alias, since
        an indirect alias can go from True to anything without conflicts, using the DOF alone."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.tirbur_free_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("tirbur_free", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_non_zero": ["tirbur"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_none_to_false_with_single_nutrient_correctly_categorises_opposing_implication(self):
        """Checks that moving from None to False with a single related nutrient correctly collects related
        nutrient in the group opposing its implication."""
        # Check direct alias first;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_with_undefined  # Choose one that doesn't mention tibur;
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("tirbur_free", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_non_zero": ["tirbur"]}
            ), conflicts)
        # Now check an DOF Flag;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_with_undefined  # Choose one that doesn't mention bar;
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("bar_free", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_non_zero": ["bar"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_true_to_none_with_direct_alias_single_nutrient_correctly_categorises_need_undefining(self):
        """This checks that going from True to False with a single nutrient correctly collects related
        nutrient in the group opposing its implication. We only do this check with a direct alias, since
        an indirect alias can go from True to anything without conflicts, using the DOF alone."""
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.tirbur_free_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("tirbur_free", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_undefining": ["tirbur"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_false_to_none_collects_all_defined_opposing_nutrients_in_need_undefining(self):
        """Checks with both direct and indirect alias flags, that moving from False to None collects
        all defined and conflicting nutrients in the 'need_undefining' collector. To move something from
        False to None, because False takes precidence, we just need to undefine the nutrients causing False."""
        # Check direct alias first;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_with_multiple_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"need_undefining": ["foo", "foobar"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_true_to_false_with_direct_alias_multiple_related_nutrients_collects_all_in_preventing_flag_false(self):
        """Checks that when we have multiple related nutrients, if we change from True to False, we
        get them all collected in 'preventing_flag_false' with both direct alias and non-direct alias
        flags."""
        # Check with direct alias first;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"preventing_flag_false": ["foo", "foobar", "foobing"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_true_to_none_with_direct_alias_multiple_related_nutrients_collects_all_in_preventing_flag_undefine(self):
        """Checks that all related nutrients get collected inside 'preventing_flag_undefine' with a direct alias
        with more than one related nutrient."""
        # Check with direct alias first;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_no_conflicts
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", None)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"preventing_flag_undefine": ["foo", "foobar", "foobing"]}
            ), conflicts)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_none_to_false_with_multiple_undefined_nutrients_collects_all_in_preventing_flag_false(self):
        """Checks that we get all undefined nutrients in preventing_flag_false, when moving from undefined
        to False with multiple nutrients undefined. This is because we don't know which of the currently
        undefined nutrients need to be converted to False, to trip the whole flag."""
        # First check with a direct alias;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.foo_free_multiple_undefined
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"preventing_flag_false": ["foo", "foobing", "foobar"]}
            ), conflicts)
        # Now check for an indirect alias;
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = self.pongaterian_with_multiple_undefined
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("pongaterian", False)
            fx.assert_nutrient_conflicts_equal(fx.make_conflicts_dict(
                {"preventing_flag_false": ["foo", "foobing", "bazing"]}
            ), conflicts)


class TestSetFlagValue(TestCase):
    @fx.use_test_flags
    def test_returns_none_if_value_didnt_change(self):
        """Make sure we get a none back if the value didn't change."""
        # Check for True;
        with mock.patch("model.flags.HasSettableFlags.get_flag_value", mock.Mock(return_value=True)):
            hr = model.flags.HasSettableFlags()
            self.assertEqual(hr.set_flag_value("foo_free", True), None)
        # Check for False;
        with mock.patch("model.flags.HasSettableFlags.get_flag_value", mock.Mock(return_value=False)):
            hr = model.flags.HasSettableFlags()
            self.assertEqual(hr.set_flag_value("foo_free", False), None)
        # Check for None;
        with mock.patch("model.flags.HasSettableFlags.get_flag_value", mock.Mock(return_value=None)):
            hr = model.flags.HasSettableFlags()
            self.assertEqual(hr.set_flag_value("foo_free", None), None)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_raises_exception_if_nutrients_in_need_non_zero(self):
        """We don't know what value to give nutrients which need non-zero values, so we
        raise an exception here."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.make_conflicts_dict({'need_non_zero': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            with self.assertRaises(model.exceptions.NonZeroNutrientRatioConflictError):
                hr.set_flag_value("foo_free", True)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_raises_exception_if_nutrients_preventing_flag_undefine(self):
        """Checks that multiple nutrient ratios potentially requiring undefine raises an exception, since
        we don't know which needs undefining."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.make_conflicts_dict({'preventing_flag_undefine': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            with self.assertRaises(model.exceptions.MultipleUndefinedRelatedNutrientRatiosError):
                hr.set_flag_value("foo_free", True)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_raises_exception_if_gets_fixable_states_without_change_permission(self):
        """Check we get an exception if we have fixable conflicts, but haven't got permission
        to adjust the related nutrient ratios on the instance."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.make_conflicts_dict({'need_zero': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            with self.assertRaises(model.exceptions.FixableNutrientRatioConflictError):
                hr.set_flag_value("foo_free", True)

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_zeros_related_nutrients_with_permission(self):
        """Check we get an exception if we have fixable conflicts, but haven't got permission
        to adjust the related nutrient ratios on the instance."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.make_conflicts_dict({'need_zero': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            hr.zero_nutrient_ratio = mock.Mock()
            hr.set_flag_value("foo_free", True, True)
            self.assertTrue(hr.zero_nutrient_ratio.call_count == 2)
            self.assertTrue(hr.zero_nutrient_ratio.call_args_list == [call("foo"), call("foobar")])

    def test_undefines_related_nutrients_with_permission(self):
        raise NotImplementedError

    def test_sets_dof_on_indirect_alias_if_no_unfixable_conflicts(self):
        raise NotImplementedError


class TestLoadData(TestCase):
    def test_loads_data_correctly(self):
        raise NotImplementedError
