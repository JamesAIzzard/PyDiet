"""Tests for the HasReadableTags class."""
from unittest import TestCase

import model.tags.exceptions
from tests.model.tags import fixtures as tfx


class TestHasTag(TestCase):
    """Tests the has_tag method."""

    def test_returns_true_if_class_has_tag(self):
        """Checks we get True if the tag is present."""
        # Create a test instance, passing in tags;
        hrt = tfx.HasReadableTagsTestable(tags=["sweet", "main", "drink"])

        # Assert we get True for a tag which is on the list;
        self.assertTrue(hrt.has_tag("sweet"))

    def test_returns_false_if_tag_not_present(self):
        """Checks we get False if the tag is not present."""
        # Create a test instance, passing in tags;
        hrt = tfx.HasReadableTagsTestable(tags=["sweet", "drink"])

        # Assert we get False for a tag which is not on the list;
        self.assertFalse(hrt.has_tag("main"))

    def test_exception_if_the_tag_is_not_recognised(self):
        """Checks we get an exception if the tag is not recognised."""
        # Create a test instance, passing in tags;
        hrt = tfx.HasReadableTagsTestable(tags=["sweet", "drink"])

        # Assert we get an exception if we pass in a tag which doesn't exist;
        with self.assertRaises(model.tags.exceptions.UnknownTagError):
            self.assertFalse(hrt.has_tag("fake"))


class TestPersistableData(TestCase):
    """Tests the persistable data property."""

    def test_returns_correct_data(self):
        """Checks the method returns the correct data."""
        # Create some tag data;
        data = ["sweet", "drink"]

        # Create a test instance, passing this data in;
        hrt = tfx.HasReadableTagsTestable(tags=data)

        # Check that we get this data back out;
        self.assertEqual(data, hrt.persistable_data['tags'])
