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
            quantity_ratio_data=qfx.get_qty_ratio_data()
        )

        # Check the instance was constructed;
        self.assertTrue(isinstance(qrob, model.quantity.IsQuantityRatioBase))


class TestRatioSubjectQty(TestCase):
    """Tests the ratio_subject_qty property."""

    def test_returns_correct_subject_instance(self):
        """Check we get the same instance out as we sent in."""
        # Create a mock subject instance;
        sub = mock.Mock()

        # Use it to create a ratio instance;
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=sub,
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=10,
                host_qty_g=20
            )
        )

        # Assert we get the same instance back if we ask for the subject;
        self.assertTrue(qrob.ratio_subject_qty.qty_subject is sub)


class TestRatioHostQty(TestCase):
    """Tests the ratio_host_qty property."""

    def test_returns_correct_instance(self):
        """Check we get the same instance out as we sent in."""
        # Create a mock host instance;
        hst = mock.Mock()

        # Use it to create a ratio instance;
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=hst,
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=10,
                host_qty_g=20
            )
        )

        # Assert we get the same instance back if we ask for the subject;
        self.assertTrue(qrob.ratio_host_qty.qty_subject is hst)


class TestSubjectGPerHostG(TestCase):
    """Tests the subject_g_per_host_g property."""

    def test_correct_value_is_returned(self):
        """Checks that we get the correct value back."""
        # Create a test instance with numerator and denominator quantities defined;
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=10,
                host_qty_g=20
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
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.1,
                subject_qty_unit="mg",
                host_qty_g=40,
                host_qty_unit='g'
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(2.5, qrob.subject_qty_in_pref_unit_per_g_of_host)


class TestSubjectQtyInPrefUnitPerRefQtyOfHost(TestCase):
    """Tests the subject_qty_in_pref_unit_per_ref_qty_of_host property."""

    def test_correct_value_is_returned(self):
        """Checks that the property returns the correct value."""
        # Create a test instance with 10mg of x per 40g of y
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.2,
                subject_qty_unit="mg",
                host_qty_g=40,
                host_qty_unit='g'
            )
        )

        # Assert we get the correct ratio;
        self.assertEqual(200, qrob.subject_qty_in_pref_unit_per_ref_qty_of_host)


class TestRatioIsDefined(TestCase):
    """Tests the ratio_is_defined property."""

    def test_returns_true_if_ratio_is_defined(self):
        """Checks that the property returns True if the ratio is defined."""
        # Create a fully defined test instance;
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=0.3,
                subject_qty_unit="mg",
                host_qty_g=40,
                host_qty_unit='g'
            )
        )

        # Assert we the property returns True;
        self.assertTrue(qrob.ratio_is_defined)

    def test_returns_false_if_ratio_is_undefined(self):
        """Checks that the property returns False if the ratio is undefined."""
        # Create a partially undefined test instance;
        qrob = qfx.IsQuantityRatioBaseTestable(
            ratio_subject=mock.Mock(),
            ratio_host=mock.Mock(),
            quantity_ratio_data=qfx.get_qty_ratio_data(
                subject_qty_g=None,
                subject_qty_unit="mg",
                host_qty_g=40,
                host_qty_unit='g'
            )
        )

        # Assert we the property returns False;
        self.assertFalse(qrob.ratio_is_defined)
