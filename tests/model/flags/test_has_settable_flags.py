"""Tests for the HasSettableFlags class."""
from unittest import TestCase, mock
from unittest.mock import call

import model
from tests.model.flags import fixtures as fx
from tests.model.nutrients import fixtures as nfx


class TestConstructor(TestCase):
    """Tests the constructor funcionality."""

    def test_can_create_instance(self):
        """Basic test just to make sure we can instantiate an instance."""
        hf = model.flags.HasSettableFlags()
        self.assertTrue(isinstance(hf, model.flags.HasSettableFlags))

    @fx.use_test_flags
    def test_calls_load_data_if_data_provided(self):
        """Check that when we pass data into the constructor, it ends up on the instance."""
        # Create an instance, passing data in;
        hsf = model.flags.HasSettableFlags(flag_data={
            "pongaterian": True,
            "foogetarian": True,
            "bar_free": False
        })

        # Confirm the flags have been set on the instance;
        self.assertTrue(hsf._get_flag_dof(flag_name="pongaterian"))
        self.assertTrue(hsf._get_flag_dof(flag_name="foogetarian"))
        self.assertFalse(hsf._get_flag_dof(flag_name="bar_free"))


class TestFlagDOFS(TestCase):
    """Tests the concrete _flag_dofs property."""

    @fx.use_test_flags
    def test_returns_local_data(self):
        """Check that we get the local data back after passing data in."""
        # Create some data;
        data = {
            "pongaterian": True,
            "foogetarian": True,
            "bar_free": False
        }

        # Create an instance, passing data in;
        hsf = model.flags.HasSettableFlags(flag_data=data)

        # Check we get the same data back;
        self.assertEqual(data, hsf._flag_dofs)


# noinspection DuplicatedCode
class TestCollectNutrientRatioConflicts(TestCase):
    """The following tests are based on the exhaustive list of scenarios listed in
    pydiet.docs.flag_conflict_logic_table.xlsx
    The test names here match test names in this table, and are ordered top to bottom.
    """

    @fx.use_test_flags
    @nfx.use_test_nutrients
    def test_no_conflicts_when_changing_state_on_dof_with_no_nutrients(self):
        """Checks that, if we have no related nutrients at all, we are free to change from any state
        to any state."""
        # Create the test instance without any nutrients;
        hsf = model.flags.HasSettableFlags()

        # Check we can change states freely without conflicts;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foogetarian", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)
        conflicts = hsf._collect_nutrient_ratio_conflicts("foogetarian", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)
        conflicts = hsf._collect_nutrient_ratio_conflicts("foogetarian", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_no_conflicts_when_changing_state_on_dof_with_all_matching_nutrients(self):
        """This checks that an indirect alias with a set of related nutrients which match the flag, can be
        changed from any state to any state. If all related nutrients match the flag, the degree of freedom is free
        to change the flag from any value to any other value."""
        # This check only applies to DOF flags.
        # Create the test instance passing in set of matching nutrient ratios;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_no_conflicts']
        )
        # Now set the flag DOF to True;
        hsf.set_flag_value("pongaterian", True)

        # Check that the flag is currently True;
        self.assertTrue(hsf.get_flag_value("pongaterian"))

        # Check we get no conflicts when transitioning to any state;
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_true_to_true_returns_no_conflicts(self):
        """This checks that going from True to True (not changing the state) always returns no conflicts, with
        a DOF and direct alias flag type."""

        # Check this works with a direct alias flag first;
        # Create the test instance, with a direct alias flag with no conflicting nutrient ratios;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_no_conflicts']
        )

        # Check the flag is currently True;
        self.assertTrue(hsf.get_flag_value("foo_free"))

        # Check we get no conflicts;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

        # Now check with a DOF flag;
        # Create the test instance, with a DOF flag with no conflicting nutrient ratios;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_no_conflicts']
        )
        # Now set the flag DOF to True;
        hsf.set_flag_value("pongaterian", True)

        # Check the flag is currently True;
        self.assertTrue(hsf.get_flag_value("pongaterian"))

        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_false_to_false_returns_no_conflicts(self):
        """This checks that going from False to False (not changing the state) always returns no conflicts, with
        a DOF and direct alias flag type."""
        # First Check this works with a direct alias flag;
        # Create the test instance, with a direct alias flag with with conflicts;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_multiple_conflicts']
        )

        # Check we get no conflicts transitioning to False (because it is already False);
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

        # Now check we get the same with a DOF flag;
        # Create the test instance, with a DOF flag with multiple conflicting nutrient ratios;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_multiple_conflicts']
        )

        # Check the flag is currently False;
        self.assertFalse(hsf.get_flag_value("pongaterian"))

        # Check we get no conflicts transitioning to False;
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_none_to_none_returns_no_conflicts(self):
        """This checks that going from None to None (not changing the state) always returns no conflicts, with
        a DOF and direct alias flag type."""

        # First check with a direct alias flag;
        # Create an instance with some undefined nutrient ratios for a direct alias flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_single_undefined']
        )

        # Assert the foo free flag is currently undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("foo_free")

        # Now check we get no conflicts against the None value;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

        # Now check with a DOF flag;
        # Now create an instance with some undefined nutrient ratios for a DOF flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_single_undefined']
        )

        # Now check we get no conflicts against the None value;
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_true_to_false_with_direct_alias_single_nutrient_correctly_categorises_opposing_implication(self):
        """This checks that going from True to False with a single nutrient correctly collects related
        nutrient in the group opposing its implication. We only do this check with a direct alias, since
        an indirect alias can go from True to anything without conflicts, using the DOF alone."""

        # Create an instance with nutrients with nutrient ratios to indicate True against a direct alias flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['tirbur_free_no_conflicts']
        )

        # Assert we have True for the flag;
        self.assertTrue(hsf.get_flag_value("tirbur_free"))

        # Assert the only related nutrient is put in the category opposite to its implication;
        conflicts = hsf._collect_nutrient_ratio_conflicts("tirbur_free", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_non_zero": ["tirbur"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_true_to_false_with_direct_alias_multiple_related_nutrients_collects_all_in_preventing_flag_false(self):
        """Checks that when we have multiple related nutrients, if we change from True to False, we
        get them all collected in 'preventing_flag_false'. We only test direct alias flags, becuase a DOF flag
        can go from True to anything without conflict."""

        # Create a test instance with multiple related nutrients, all driving True on the flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_no_conflicts']
        )

        # Make sure the falg is True;
        self.assertTrue(hsf.get_flag_value("foo_free"))

        # Now check we get all related nutrients in preventing_flag_false;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"preventing_flag_false": ["foo", "foobar", "foobing"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_true_to_none_with_direct_alias_single_nutrient_correctly_categorises_need_undefining(self):
        """This checks that going from True to False with a single nutrient correctly collects related
        nutrient in the group opposing its implication. We only do this check with a direct alias, since
        a DOF flag can go from True to anything without conflicts, using the DOF alone."""
        # Create a test instance with nutrient ratios matching True for a flag with only one relation;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['tirbur_free_no_conflicts']
        )

        # Check that the flag is currently True;
        self.assertTrue(hsf.get_flag_value("tirbur_free"))

        # Now check we get the only related nutrient in need_undefining, against proposed value of None;
        conflicts = hsf._collect_nutrient_ratio_conflicts("tirbur_free", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_undefining": ["tirbur"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_true_to_none_with_direct_alias_multiple_related_nutrients_collects_all_in_preventing_flag_undefine(self):
        """Checks that all related nutrients get collected inside 'preventing_flag_undefine' with a direct alias
        with more than one related nutrient."""

        # Create a test instance with multiple related nutrients, all driving True on the flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_no_conflicts']
        )

        # Make sure the flag is True;
        self.assertTrue(hsf.get_flag_value("foo_free"))

        # Now check we get all related nutrients in preventing_undefine if we propose False;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"preventing_flag_undefine": ["foo", "foobar", "foobing"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_none_to_true_correctly_categorises_nutrients(self):
        """This checks that going from None to True correctly collects related
        nutrients into need_zero and need_non_zero to match their implications."""
        # First check with a direct alias flag;
        # Create an instance with some undefined nutrient ratios for a direct alias flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_single_undefined']
        )

        # Assert the flag is currently undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("foo_free")

        # Now check we get the right conflicts against a True flag;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_zero": ["foobar"]}
        ), conflicts)

        # Now check with a DOF flag;
        # Create an instance with some undefined nutrient ratios for a DOF flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_single_undefined']
        )

        # Assert the flag is currently undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("pongaterian")

        # Now check we get the right conflicts against a True flag;
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_non_zero": ["bazing"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_none_to_false_with_single_nutrient_correctly_categorises_opposing_implication(self):
        """Checks that moving from None to False with a single related nutrient correctly collects related
        nutrient in the group opposing its implication."""

        # First test a direct alias flag;
        # Create an instance with nutrient ratios to make a direct alias flag with a single relation
        # return None;
        # foo_free doesn't mention tirbur, so we pass in foo_free nr's and test against the tirbur flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_single_undefined']
        )

        # Assert that tirbur_free comes up undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("tirbur_free")

        # Now assert that we get the only nutrient ratio for tirbur_free in the group which
        # opposes its implication, against a flag value of False;
        conflicts = hsf._collect_nutrient_ratio_conflicts("tirbur_free", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_non_zero": ["tirbur"]}
        ), conflicts)

        # Now check an DOF Flag;
        # foo_free doesn't mention bar either, so create the test instance with those nutrient ratios;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_single_undefined']
        )

        # Assert that bar comes up undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("bar_free")

        # bar is zero for bar_free, so assert that we get bar in need_non_zero, to match False;
        conflicts = hsf._collect_nutrient_ratio_conflicts("bar_free", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_non_zero": ["bar"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_none_to_false_with_multiple_undefined_nutrients_collects_all_in_preventing_flag_false(self):
        """Checks that we get all related nutrients in preventing_flag_false, when moving from undefined
        to False. This is because we don't know which of the nutrients need to oppose the flag in
        order to trip the whole flag."""
        # First check with a direct alias flag;
        # Create a test instance with multiple nutrients causing a direct flag to be undefined;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_multiple_undefined']
        )

        # Check the flag is actually undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("foo_free")

        # Now check we get all related nutrients in preventing_flag_false, if we propose False;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"preventing_flag_false": ["foo", "foobing", "foobar"]}
        ), conflicts)

        # Now check with a DOF flag;
        # Create a test instance with multiple nutrients causing a DOF flag to be undefined;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_multiple_undefined']
        )

        # Check the flag is actually undefined;
        with self.assertRaises(model.flags.exceptions.UndefinedFlagError):
            _ = hsf.get_flag_value("pongaterian")

        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", False)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"preventing_flag_false": ["foo", "foobing", "bazing"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_false_to_true_correctly_categorises_nutrients(self):
        """This checks that going from False to True correctly collects related
        nutrients into need_zero and need_non_zero to match their implications."""

        # First check with a direct alias flag;
        # Create an instance with multiple nutrient ratios that conflict against a direct alias flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_multiple_conflicts']
        )

        # Check the flag is False;
        self.assertFalse(hsf.get_flag_value("foo_free"))

        # Now check we get the right conflicts against the foo-free flag;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_zero": ["foo", "foobar"]}
        ), conflicts)

        # Now check with a DOF flag;
        # Now create an instance with nutrient ratios that conflict against a DOF flag;
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_multiple_conflicts']
        )

        # Check the flag is False;
        self.assertFalse(hsf.get_flag_value("pongaterian"))

        # Now check we get the right conflicts for True against the currently False flag;
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", True)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_zero": ["foobing"], "need_non_zero": ["bazing"]}
        ), conflicts)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_false_to_none_collects_all_defined_opposing_nutrients_in_need_undefining(self):
        """Checks with both direct and indirect alias flags, that moving from False to None collects
        all defined and conflicting nutrients in the 'need_undefining' collector. To move something from
        False to None, because False takes precidence, we just need to undefine the nutrients causing False."""
        # First check with a direct alias flag;
        # Create an instance with multiple nutrient ratios causing False on a direct_alias flag.
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['foo_free_multiple_conflicts']
        )

        # Check the flag comes up False;
        self.assertFalse(hsf.get_flag_value("foo_free"))

        # Check all opposing nutrients end up in need_undefining;
        conflicts = hsf._collect_nutrient_ratio_conflicts("foo_free", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_undefining": ["foo", "foobar"]}
        ), conflicts)

        # Now check with a DOF flag;
        # Now create an instance with multiple nutrient ratios causing False on a DOF flag.
        hsf = model.flags.HasSettableFlags(
            nutrient_ratios_data=fx.FLAG_NR_SCENARIOS['pongaterian_multiple_conflicts']
        )

        # Check the flag comes up False;
        self.assertFalse(hsf.get_flag_value("pongaterian"))

        # Check all opposing nutrients end up in need_undefining;
        # Check all opposing nutrients end up in need_undefining;
        conflicts = hsf._collect_nutrient_ratio_conflicts("pongaterian", None)
        fx.assert_nutrient_conflicts_equal(fx.get_conflicts_dict(
            {"need_undefining": ["foobing", "bazing"]}
        ), conflicts)


# noinspection DuplicatedCode
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
    @fx.nfx.use_test_nutrients
    def test_raises_exception_if_nutrients_in_need_non_zero(self):
        """We don't know what value to give nutrients which need non-zero values, so we
        raise an exception here."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.get_conflicts_dict({'need_non_zero': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            with self.assertRaises(model.exceptions.NonZeroNutrientRatioConflictError):
                hr.set_flag_value("foo_free", True)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_raises_exception_if_nutrients_preventing_flag_undefine(self):
        """Checks that multiple nutrient ratios potentially requiring undefine raises an exception, since
        we don't know which needs undefining."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.get_conflicts_dict({'preventing_flag_undefine': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            with self.assertRaises(model.exceptions.MultipleUndefinedRelatedNutrientRatiosError):
                hr.set_flag_value("foo_free", True)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_raises_exception_if_gets_fixable_states_without_change_permission(self):
        """Check we get an exception if we have fixable conflicts, but haven't got permission
        to adjust the related nutrient ratios on the instance."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.get_conflicts_dict({'need_zero': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            with self.assertRaises(model.exceptions.FixableNutrientRatioConflictError):
                hr.set_flag_value("foo_free", True)

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_zeros_related_nutrients_with_permission(self):
        """Checks zero_nutrient is called if nutrients require zeroing, and we have permission to
        change them."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.get_conflicts_dict({'need_zero': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            hr.zero_nutrient_ratio = mock.Mock()
            hr.set_flag_value("foo_free", True, True)
            self.assertTrue(hr.zero_nutrient_ratio.call_count == 2)
            self.assertTrue(hr.zero_nutrient_ratio.call_args_list == [call("foo"), call("foobar")])

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_undefines_related_nutrients_with_permission(self):
        """Checks undefine_nutrient is called if nutrients require undefining, and we have permission
         to change them."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.get_conflicts_dict({'need_undefining': ["foo", "foobar"]})
        )):
            hr = model.flags.HasSettableFlags()
            hr.undefine_nutrient_ratio = mock.Mock()
            hr.set_flag_value("foo_free", True, True)
            self.assertTrue(hr.undefine_nutrient_ratio.call_count == 2)
            self.assertTrue(hr.undefine_nutrient_ratio.call_args_list == [call("foo"), call("foobar")])

    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_sets_dof_on_indirect_alias_if_no_unfixable_conflicts(self):
        """Checks the flag dof is set on an indirect alias if there are no remaining unresolved
        conflicts with the flag state."""
        with mock.patch("model.flags.HasSettableFlags._collect_nutrient_ratio_conflicts", mock.Mock(
                return_value=fx.get_conflicts_dict()
        )):
            hr = model.flags.HasSettableFlags()
            hr.set_flag_value("bar_free", False)
            self.assertTrue(hr._flag_dofs["bar_free"] is False)
            hr.set_flag_value("bar_free", True)
            self.assertTrue(hr._flag_dofs["bar_free"] is True)


class TestLoadData(TestCase):
    @fx.use_test_flags
    @fx.nfx.use_test_nutrients
    def test_loads_data_correctly(self):
        """Checks that flag dof data is loaded into the instance correctly."""
        hr = model.flags.HasSettableFlags()
        hr.load_data({"flag_data": {
            'foogetarian': True,
            'bar_free': False,
            'foo_free': False  # Should be ignored, not a DOF.
        }})
        self.assertEqual(hr._flag_dofs, {
            'foogetarian': True,
            'bar_free': False
        })
