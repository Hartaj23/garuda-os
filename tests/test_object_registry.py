import unittest

from packages.objects import CanonicalObject, GarudaObject, ObjectRegistry, ObjectFactory


class ExampleCanonicalObject(CanonicalObject):
    pass


class ExampleNonCanonicalObject(GarudaObject):
    pass


class ObjectRegistryTest(unittest.TestCase):
    def test_registers_canonical_object_types(self) -> None:
        registry = ObjectRegistry()
        registry.register(ExampleCanonicalObject)
        self.assertEqual(registry.lookup("ExampleCanonicalObject"), ExampleCanonicalObject)

    def test_rejects_non_canonical_types(self) -> None:
        registry = ObjectRegistry()
        with self.assertRaises(TypeError):
            registry.register(ExampleNonCanonicalObject)

    def test_rejects_duplicate_registration(self) -> None:
        registry = ObjectRegistry()
        registry.register(ExampleCanonicalObject)
        with self.assertRaises(ValueError):
            registry.register(ExampleCanonicalObject)

    def test_lookup_by_class(self) -> None:
        registry = ObjectRegistry()
        registry.register(ExampleCanonicalObject)
        self.assertEqual(registry.lookup_by_class(ExampleCanonicalObject), ExampleCanonicalObject)

    def test_enumerates_registered_types(self) -> None:
        registry = ObjectRegistry()
        registry.register(ExampleCanonicalObject)
        self.assertEqual(registry.enumerate(), (ExampleCanonicalObject,))

    def test_validate_accepts_only_canonical_types(self) -> None:
        registry = ObjectRegistry()
        registry.register(ExampleCanonicalObject)
        registry.validate()

    def test_factory_placeholder_is_inert(self) -> None:
        factory = ObjectFactory()
        with self.assertRaises(NotImplementedError):
            factory.create()


if __name__ == "__main__":
    unittest.main()
