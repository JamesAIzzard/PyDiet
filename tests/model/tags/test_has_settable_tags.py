"""Tests for the HasSettableTags class."""
from unittest import TestCase

import model


class TestConstructor(TestCase):
    """Tests for the constructor function."""

    def test_can_create_simple_instance(self):
        """Checks we can create a simple instance."""
        self.assertTrue(model.tags.HasSettableTags(), model.tags.HasSettableTags)

    def test_data_loaded_if_passed_in(self):
        """Checks any data passed to the constructor gets loaded."""
        # Create some test data;
        data = ["sweet", "main"]

        # Create a new instance, passing the data in;
        hst = model.tags.HasSettableTags(tag_data=data)

        # Check that the data is now on the instance;
        self.assertEqual(set(data), set(hst.tags))

    def test_exception_if_data_passed_in_is_invalid(self):
        """Checks that any data we pass in is invalid."""
        # Create some test data, with an invalid tag;;
        data = ["sweet", "fake"]

        # Check we get an exception if we try to create with this data;
        with self.assertRaises(model.tags.exceptions.UnknownTagError):
            hst = model.tags.HasSettableTags(tag_data=data)


class TestTags(TestCase):
    """Tests for the tags property."""

    def test_tags_returned_correctly(self):
        """Check the tags are returned correctly."""
        # Create some test data;
        data = ["sweet", "main"]

        # Create a new instance, passing the data in;
        hst = model.tags.HasSettableTags(tag_data=data)

        # Check that the data is now on the instance;
        self.assertEqual(set(data), set(hst.tags))


class TestAddTags(TestCase):
    """Tests for the add_tags method."""

    def test_adds_tags_correctly(self):
        """Check the tags are added correctly."""
        # Create an empty instance;
        hst = model.tags.HasSettableTags()

        # Assert there are no tags;
        self.assertEqual(0, len(hst.tags))

        # Add a tag;
        hst.add_tags(["sweet"])

        # Assert the tag was added;
        self.assertEqual(1, len(hst.tags))
        self.assertEqual("sweet", hst.tags[0])

    def test_exception_if_tag_is_invalid(self):
        """Checks we get an exception if we try to add a tag not on the global list."""
        # Create an empty instance;
        hst = model.tags.HasSettableTags()

        # Check we get an exception if we try to add a tag that isn't on the list;
        with self.assertRaises(model.tags.exceptions.UnknownTagError):
            hst.add_tags(["fake"])

    def test_does_not_duplicate_tags_already_on_list(self):
        """Checks that any tags already on the list do not get duplicated."""
        # Create some test data;
        data = ["sweet", "main"]

        # Create a new instance, passing the data in;
        hst = model.tags.HasSettableTags(tag_data=data)

        # Check the tags are as they should be;
        self.assertEqual(data, hst.tags)

        # Now try and add one of those tags again;
        hst.add_tags(["sweet"])

        # Check there are no changes to the data;
        self.assertEqual(data, hst.tags)


class TestLoadData(TestCase):
    """Tests for teh load_data property."""

    def test_loads_data_correctly(self):
        """Checks that any data submitted gets loaded onto the instance correctly."""
        # Create some test data;
        data = ["sweet", "main"]

        # Create an empty instance;
        hst = model.tags.HasSettableTags()

        # Check the instance has no data;
        self.assertEqual(0, len(hst.tags))

        # Load the data;
        hst.load_data({"tags": data})

        # Check that the data is now on the instance;
        self.assertEqual(set(data), set(hst.tags))

    def test_exception_if_data_contains_unrecognised_tags(self):
        """Checks that we get an exception if we try to load data containing unrecognised tags."""
        # Create some test data;
        data = ["sweet", "fake"]

        # Create an empty instance;
        hst = model.tags.HasSettableTags()

        # Check we get an exception when we try to load the faulty data;
        with self.assertRaises(model.tags.exceptions.UnknownTagError):
            hst.load_data({"tags": data})

