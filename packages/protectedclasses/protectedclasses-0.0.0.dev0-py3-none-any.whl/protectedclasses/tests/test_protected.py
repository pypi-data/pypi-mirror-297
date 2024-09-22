import unittest

from protectedclasses import ProtectedClass


class TestProtectedClass(unittest.TestCase):

    class TestClass(ProtectedClass):
        def __init__(self):
            self._private_attr = 0
            self._another_private_attr = "hidden"

        @property
        def public_property(self):
            return "This is a public property"

        @public_property.setter
        def public_property(self, value):
            self._set_property = value

    def setUp(self):
        # Create an instance of TestClass before each test
        self.obj = self.TestClass()

    # Test if private attributes (those that start with an underscore) can be set
    def test_set_private_attribute(self):
        self.obj._private_attr = 10
        self.assertEqual(self.obj._private_attr, 10)

    # Test setting an attribute that is a property
    def test_set_property(self):
        self.obj.public_property = "new value"
        self.assertEqual(self.obj._set_property, "new value")

    # Test accessing an existing private attribute
    def test_get_private_attribute(self):
        self.assertEqual(self.obj._another_private_attr, "hidden")

    # Test attempting to set an attribute that does not exist and is not a property
    def test_set_invalid_attribute(self):
        with self.assertRaises(AttributeError) as cm:
            self.obj.some_invalid_attribute = 5
        self.assertEqual(
            str(cm.exception),
            "'TestClass' object has no property 'some_invalid_attribute'",
        )

    # Test error message format when setting an invalid attribute
    def test_error_message_format(self):
        with self.assertRaises(AttributeError) as cm:
            self.obj.another_invalid_attr = "invalid"
        self.assertEqual(
            str(cm.exception),
            "'TestClass' object has no property 'another_invalid_attr'",
        )

    # Test that the error is raised for non-property and non-underscore attributes
    def test_set_non_property_attribute(self):
        with self.assertRaises(AttributeError):
            self.obj.random_attribute = "random_value"

    # Test that setting property correctly works
    def test_property_setter(self):
        self.obj.public_property = "set value"
        self.assertEqual(self.obj._set_property, "set value")

    # Test that no error is raised for setting existing private attributes
    def test_no_error_for_private_attribute(self):
        try:
            self.obj._private_attr = 42
        except AttributeError:
            self.fail(
                "AttributeError raised unexpectedly when setting a private attribute."
            )

    # Test setting a private attribute doesn't raise an error even after multiple changes
    def test_multiple_private_attr_changes(self):
        self.obj._private_attr = 100
        self.assertEqual(self.obj._private_attr, 100)
        self.obj._private_attr = 200
        self.assertEqual(self.obj._private_attr, 200)

    # Test that properties are read-only unless setters are defined
    def test_read_only_property_without_setter(self):
        self.assertEqual(self.obj.public_property, "This is a public property")


if __name__ == "__main__":
    unittest.main()
