import unittest

from packages.objects import (
    GarudaObject,
    ValidationCategory,
    ValidationError,
    ValidationResult,
    ValidationSeverity,
    validate_object,
)


class ValidationFrameworkTest(unittest.TestCase):
    def test_validation_severity_levels_are_platform_values(self) -> None:
        self.assertEqual(
            {item.value for item in ValidationSeverity},
            {"info", "warning", "error", "critical"},
        )

    def test_validation_categories_are_platform_values(self) -> None:
        self.assertEqual(
            {item.value for item in ValidationCategory},
            {
                "identity",
                "metadata",
                "lifecycle",
                "behavior",
                "relationships",
                "schema",
                "version",
            },
        )

    def test_validation_error_preserves_required_fields(self) -> None:
        error = ValidationError(
            message="Schema version is required.",
            category=ValidationCategory.SCHEMA,
            field="schema_version",
            code="missing_schema_version",
            context={"source": "unit-test"},
        )
        self.assertEqual(error.message, "Schema version is required.")
        self.assertEqual(error.category, ValidationCategory.SCHEMA)
        self.assertEqual(error.severity, ValidationSeverity.ERROR)
        self.assertEqual(error.field, "schema_version")
        self.assertEqual(error.code, "missing_schema_version")
        self.assertEqual(error.context, {"source": "unit-test"})

    def test_validation_result_tracks_validity_by_error_severity(self) -> None:
        result = ValidationResult()
        self.assertTrue(result.is_valid)

        result.add_warning("Metadata is sparse.", ValidationCategory.METADATA)
        self.assertTrue(result.is_valid)

        result.add_error("Object version is invalid.", ValidationCategory.VERSION)
        self.assertFalse(result.is_valid)

    def test_validation_result_merges_results_and_errors(self) -> None:
        result = ValidationResult()
        other = ValidationResult(
            errors=[
                ValidationError(
                    message="Lifecycle is invalid.",
                    category=ValidationCategory.LIFECYCLE,
                )
            ]
        )
        direct_error = ValidationError(
            message="Relationship map is invalid.",
            category=ValidationCategory.RELATIONSHIPS,
        )

        result.merge(other)
        result.merge(direct_error)
        result.merge(None)

        self.assertEqual(
            [error.category for error in result.errors],
            [
                ValidationCategory.LIFECYCLE,
                ValidationCategory.RELATIONSHIPS,
            ],
        )

    def test_validate_object_accepts_default_garuda_object(self) -> None:
        result = validate_object(GarudaObject())
        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors, [])

    def test_validate_object_reports_platform_invariant_errors(self) -> None:
        obj = GarudaObject()
        obj.schema_version = ""
        obj.object_version = 0

        result = validate_object(obj)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.category for error in result.errors},
            {ValidationCategory.SCHEMA, ValidationCategory.VERSION},
        )

    def test_garuda_object_validate_runs_existing_none_returning_hooks(self) -> None:
        calls: list[str] = []

        def hook(obj: GarudaObject) -> None:
            calls.append(obj.object_type)

        obj = GarudaObject()
        obj.register_validation_hook(hook)
        result = obj.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(calls, ["GarudaObject"])

    def test_garuda_object_validate_preserves_exception_based_hooks(self) -> None:
        def hook(obj: GarudaObject) -> None:
            raise ValueError(f"{obj.object_type} failed validation")

        obj = GarudaObject()
        obj.register_validation_hook(hook)

        with self.assertRaises(ValueError):
            obj.validate()

    def test_garuda_object_validate_merges_hook_returned_validation_error(self) -> None:
        def hook(obj: GarudaObject) -> ValidationError:
            return ValidationError(
                message=f"{obj.object_type} hook failed.",
                category=ValidationCategory.BEHAVIOR,
            )

        obj = GarudaObject()
        obj.register_validation_hook(hook)
        result = obj.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].category, ValidationCategory.BEHAVIOR)

    def test_garuda_object_validate_merges_hook_returned_validation_result(self) -> None:
        def hook(obj: GarudaObject) -> ValidationResult:
            result = ValidationResult()
            result.add_warning(
                f"{obj.object_type} has no optional metadata.",
                ValidationCategory.METADATA,
            )
            return result

        obj = GarudaObject()
        obj.register_validation_hook(hook)
        result = obj.validate()

        self.assertTrue(result.is_valid)
        self.assertEqual(result.errors[0].severity, ValidationSeverity.WARNING)


if __name__ == "__main__":
    unittest.main()
