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
    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_returns_empty_lists_if_no_conflict_when_flag_true(self):
        """This is a straighforward check to make sure we don't get conflicts if our nutrient ratios
        already match a True flag, if the flag is being set to True.
        """
        nutrient_ratios = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.9),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4)
        }
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = nutrient_ratios
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", True)
            self.assertEqual(
                conflicts,
                {
                    "need_zero": [],
                    "need_non_zero": [],
                    "need_undefining": [],
                    "preventing_flag_undefine": []
                }
            )

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_returns_empty_lists_if_no_conflict_when_flag_false(self):
        """This is a straighforward check to make sure we don't get conflicts if our nutrient ratios
        already match a False flag, if the flag is being set to False.
        """
        nutrient_ratios = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0.1),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0.2),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4),
        }
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = nutrient_ratios
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", False)
            self.assertEqual(
                conflicts,
                {
                    "need_zero": [],
                    "need_non_zero": [],
                    "need_undefining": [],
                    "preventing_flag_undefine": []
                }
            )

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_returns_empty_lists_if_flag_already_undefined_when_setting_to_undefined(self):
        """This is a straighforward check to make sure we don't get conflicts if some of the nutrient
        ratios are undefined, but we are setting the flag to undefined.
        """
        nutrient_ratios = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0.4),
        }
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = nutrient_ratios
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", None)
            self.assertEqual(
                conflicts,
                {
                    "need_zero": [],
                    "need_non_zero": [],
                    "need_undefining": [],
                    "preventing_flag_undefine": []
                }
            )

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_direct_alias_returns_correct_conflicts_if_flag_value_true_and_some_nutrient_ratios_conflict(self):
        """Checks that the conflicts are categorised correctly, if we set the flag to True, and some
        of the nutrient ratios do conflict."""
        nutrient_ratios = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0.9),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.5),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0),
            "bazing": fx.get_mock_nutrient_ratio("bazing", 0),
            "busskie": fx.get_mock_nutrient_ratio("busskie", 0)
        }
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = nutrient_ratios
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("conflict_tester", True)
            self.assertEqual(
                conflicts,
                {
                    "need_zero": ["foo", "tirbur"],
                    "need_non_zero": ["busskie", "bazing"],
                    "need_undefining": [],
                    "preventing_flag_undefine": []
                }
            )

    @fx.use_test_flags
    @fx.nutfx.use_test_nutrients
    def test_direct_alias_returns_correct_conflicts_if_flag_value_false(self):
        """This checks that the conflicts are categorised correctly if we set the flag to False
        and ALL of the flag values are True.
        """
        # We are setting to false here.
        nutrient_ratios = {
            "foo": fx.get_mock_nutrient_ratio("foo", 0),
            "foobing": fx.get_mock_nutrient_ratio("foobing", 0.5),
            "foobar": fx.get_mock_nutrient_ratio("foobar", 0)
        }
        with mock.patch("model.flags.HasSettableFlags.nutrient_ratios",
                        new_callable=mock.PropertyMock) as mock_nrs:
            mock_nrs.return_value = nutrient_ratios
            hf = model.flags.HasSettableFlags()
            conflicts = hf._collect_nutrient_ratio_conflicts("foo_free", False)
            self.assertEqual(
                conflicts,
                {
                    "need_zero": ["foobing"],
                    "need_non_zero": ["foo", "foobar"],
                    "need_undefining": [],
                    "preventing_flag_undefine": []
                }
            )
