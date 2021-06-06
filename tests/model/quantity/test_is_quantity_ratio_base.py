"""Defines tests for the IsQuantityRatioBase class."""
from unittest import TestCase, mock

import model
from tests.model.quantity import fixtures as qfx


class TestConstructor(TestCase):
    """Tests the constructor function."""

    def test_can_construct_instance(self):
        """Checks that we can construct an instance."""
        # Create a simple test insance;
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),

            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
            ),
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data())
            )
        )

        # Check the instance was constructed;
        self.assertTrue(isinstance(qrob, model.quantity.IsQuantityRatioOf))

    def test_exception_if_subject_qty_greater_than_host_qty(self):
        """Checks that we can't construct an instance where the subject quantity is greater than
        the host quantity."""
        # Assert we get an exception if we try to create a quantity ratio where the
        # subject quantity is greater than the host quantity;
        with self.assertRaises(model.quantity.exceptions.SubjectQtyExceedsHostQtyError):
            _ = model.quantity.IsQuantityRatioOf(
                subject_qty=model.quantity.IsReadonlyQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=100))
                ),
                host_qty=model.quantity.IsReadonlyQuantityOf(
                    qty_subject=mock.Mock(),
                    quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=20))
                )
            )


class TestRatioSubjectQty(TestCase):
    """Tests the ratio_subject_qty property."""

    def test_returns_correct_instance(self):
        """Check we get the same instance out as we sent in."""
        # Create a mock subject instance;
        sub_qty = model.quantity.IsReadonlyQuantityOf(
            qty_subject=mock.Mock(),
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=10))
        )

        # Use it to create a ratio instance;
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=sub_qty,
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=20))
            )
        )

        # Assert we get the same instance back if we ask for the subject;
        self.assertTrue(qrob.ratio_subject_qty is sub_qty)


class TestRatioHostQty(TestCase):
    """Tests the ratio_host_qty property."""

    def test_returns_correct_instance(self):
        """Check we get the same instance out as we sent in."""
        # Create a mock subject instance;
        host_qty = model.quantity.IsReadonlyQuantityOf(
            qty_subject=mock.Mock(),
            quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=10))
        )

        # Use it to create a ratio instance;
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=20))
            ),
            host_qty=host_qty
        )

        # Assert we get the same instance back if we ask for the subject;
        self.assertTrue(qrob.ratio_host_qty is host_qty)


class TestSubjectGPerHostG(TestCase):
    """Tests the subject_g_per_host_g property."""

    def test_correct_value_is_returned(self):
        """Checks that we get the correct value back."""
        # Create a test instance with numerator and denominator quantities defined;
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=10))
            ),
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=20))
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(0.5, qrob.subject_g_per_host_g)


class TestSubjectQtyInPrefUnitPerGOfHost(TestCase):
    """Tests the subject_qty_in_pref_unit_per_g_of_host property."""

    def test_correct_value_is_returned(self):
        """Checks that the property returns the correct value."""
        # OK, lets simulate a ratio with 10mg of x for every 40g of y.
        # Create a testable instance to represent this scenario;
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=0.01, pref_unit='mg'))
            ),
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(0.25, qrob.subject_qty_in_pref_unit_per_g_of_host)


class TestSubjectQtyInPrefUnitPerRefQtyOfHost(TestCase):
    """Tests the subject_qty_in_pref_unit_per_ref_qty_of_host property."""

    def test_correct_value_is_returned(self):
        """Checks that the property returns the correct value."""
        # Create a test instance with 10mg of x per 40g of y
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=0.02, pref_unit='mg'))
            ),
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(20, qrob.subject_qty_in_pref_unit_per_ref_qty_of_host)


class TestRatioIsDefined(TestCase):
    """Tests the ratio_is_defined property."""

    def test_returns_true_if_ratio_is_defined(self):
        """Checks that the property returns True if the ratio is defined."""
        # Create a fully defined test instance;
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=0.03, pref_unit='mg'))
            ),
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we the property returns True;
        self.assertTrue(qrob.ratio_is_defined)

    def test_returns_false_if_ratio_is_undefined(self):
        """Checks that the property returns False if the ratio is undefined."""
        # Create a partially undefined test instance;
        qrob = model.quantity.IsQuantityRatioOf(
            subject_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=None, pref_unit='mg'))
            ),
            host_qty=model.quantity.IsReadonlyQuantityOf(
                qty_subject=mock.Mock(),
                quantity_data_src=qfx.get_qty_data_src(qfx.get_qty_data(qty_in_g=40, pref_unit='g'))
            )
        )

        # Assert we the property returns False;
        self.assertFalse(qrob.ratio_is_defined)
