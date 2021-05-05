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
    def test_returns_empty_lists_if_no_conflict(self):
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
