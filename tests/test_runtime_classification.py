import unittest
from datetime import datetime
from uuid import UUID

from packages.objects import CanonicalObject, ObjectSerializer, ValidationResult
from packages.runtime import (
    CanonicalRuntimeContextClassification,
    RuntimeClassificationMetadata,
    RuntimeContextClassification,
    RuntimeContextClassificationHook,
    RuntimeContextClassificationHookCollection,
    RuntimeContextReference,
    RuntimeContractMetadata,
    evaluate_runtime_context_classification,
    validate_canonical_runtime_context_classification,
)


TIMESTAMP = datetime.fromisoformat("2026-07-07T00:00:00+00:00")


def build_context_reference() -> RuntimeContextReference:
    return RuntimeContextReference(
        context_identifier="context:00000000-0000-0000-0000-000000006001",
        context_metadata=RuntimeContractMetadata(values={"scope": "runtime"}),
    )


def build_classification_hook() -> RuntimeContextClassificationHook:
    return RuntimeContextClassificationHook(
        context_reference=build_context_reference(),
        classification=RuntimeContextClassification.EXTERNAL_FACING,
        classification_metadata=RuntimeClassificationMetadata(values={"mission": "delta"}),
    )


def build_classification_record() -> CanonicalRuntimeContextClassification:
    primary_reference = build_context_reference()
    return CanonicalRuntimeContextClassification(
        object_id=UUID("00000000-0000-0000-0000-000000006002"),
        context_reference=primary_reference,
        classification=RuntimeContextClassification.EXTERNAL_FACING,
        classification_hooks=RuntimeContextClassificationHookCollection(
            hooks=(
                RuntimeContextClassificationHook(
                    context_reference=primary_reference,
                    classification=RuntimeContextClassification.EXTERNAL_FACING,
                ),
                RuntimeContextClassificationHook(
                    context_reference=RuntimeContextReference(
                        context_identifier="context:00000000-0000-0000-0000-000000006003",
                    ),
                    classification=RuntimeContextClassification.ASSOCIATED,
                ),
            )
        ),
        classification_metadata=RuntimeClassificationMetadata(values={"taxonomy": "runtime"}),
        metadata={"owner": "runtime"},
        tags=["runtime", "delta"],
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class RuntimeClassificationTest(unittest.TestCase):
    def test_package_exports_import_cleanly(self) -> None:
        import packages.runtime as runtime_pkg

        for symbol in (
            "CanonicalRuntimeContextClassification",
            "RuntimeClassificationMetadata",
            "RuntimeContextClassification",
            "RuntimeContextClassificationHook",
            "RuntimeContextClassificationHookCollection",
            "RuntimeContextClassificationEvaluation",
            "evaluate_runtime_context_classification",
        ):
            self.assertIn(symbol, runtime_pkg.__all__)
            self.assertTrue(hasattr(runtime_pkg, symbol))

    def test_classification_record_inherits_platform_core(self) -> None:
        record = build_classification_record()

        self.assertIsInstance(record, CanonicalObject)
        self.assertEqual(record.object_type, "CanonicalRuntimeContextClassification")

    def test_canonical_serialization_without_custom_adapters(self) -> None:
        record = build_classification_record()

        core_payload = ObjectSerializer.serialize(record)
        record_payload = record.to_dict()

        self.assertEqual(core_payload["object_type"], "CanonicalRuntimeContextClassification")
        self.assertEqual(record_payload["classification"], "external_facing")

    def test_platform_validation_passes(self) -> None:
        self.assertTrue(build_classification_record().validate().is_valid)

    def test_classification_evaluation_is_deterministic_and_pure(self) -> None:
        hook = build_classification_hook()

        first = evaluate_runtime_context_classification(hook)
        second = evaluate_runtime_context_classification(hook)

        self.assertEqual(first.to_dict(), second.to_dict())
        self.assertEqual(first.classification, "external_facing")
        self.assertEqual(
            first.context_identifier,
            "context:00000000-0000-0000-0000-000000006001",
        )

    def test_classification_hooks_are_technology_neutral(self) -> None:
        record = build_classification_record()
        hook = record.classification_hooks.hooks[0]

        self.assertEqual(hook.classification, RuntimeContextClassification.EXTERNAL_FACING)
        self.assertNotIn("http", hook.context_reference.context_identifier.lower())
        self.assertNotIn("provider", hook.classification.value)
        self.assertNotIn("engine", str(hook.to_dict()).lower())

    def test_classification_enum_values_are_deterministic_and_serializable(self) -> None:
        metadata = RuntimeClassificationMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        self.assertEqual(RuntimeContextClassification.GOVERNED.value, "governed")

    def test_classification_hook_validation_reports_invalid_classification(self) -> None:
        record = build_classification_record()
        record._classification = "external_facing"

        result = record.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "classification")

    def test_classification_hook_validation_reports_invalid_context_reference(self) -> None:
        record = build_classification_record()
        record._context_reference = RuntimeContextReference(context_identifier="")

        result = record.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(result.errors[0].field, "context_reference.context_identifier")

    def test_classification_hook_collection_validation_reports_invalid_hook(self) -> None:
        record = build_classification_record()
        record._classification_hooks = RuntimeContextClassificationHookCollection(
            hooks=(
                RuntimeContextClassificationHook(
                    context_reference=RuntimeContextReference(context_identifier=""),
                    classification=RuntimeContextClassification.NEUTRAL,
                ),
            )
        )

        result = record.validate()

        self.assertFalse(result.is_valid)
        self.assertEqual(
            result.errors[0].field,
            "classification_hooks.hooks[0].context_reference.context_identifier",
        )

    def test_evaluation_rejects_invalid_hook(self) -> None:
        hook = RuntimeContextClassificationHook(
            context_reference=RuntimeContextReference(context_identifier=""),
            classification=RuntimeContextClassification.NEUTRAL,
        )

        with self.assertRaises(ValueError):
            evaluate_runtime_context_classification(hook)

    def test_validate_helper_returns_validation_result(self) -> None:
        record = build_classification_record()
        record._classification_metadata = "invalid"

        result = validate_canonical_runtime_context_classification(record)

        self.assertIsInstance(result, ValidationResult)
        self.assertFalse(result.is_valid)

    def test_classification_to_dict_is_deterministic(self) -> None:
        record = build_classification_record()

        first = record.to_dict()
        second = record.to_dict()

        self.assertEqual(first, second)
        self.assertEqual(first["classification"], "external_facing")
        self.assertEqual(len(first["classification_hooks"]["hooks"]), 2)

    def test_no_cognitive_foundation_imports_in_classification_modules(self) -> None:
        import packages.runtime.classification.evaluation as evaluation_module
        import packages.runtime.classification.metadata as metadata_module
        import packages.runtime.classification.record as record_module
        import packages.runtime.classification.taxonomy as taxonomy_module

        forbidden_prefixes = (
            "packages.memory",
            "packages.knowledge",
            "packages.context",
            "packages.reasoning",
            "packages.decision",
            "packages.action",
            "packages.execution",
        )

        for module in (metadata_module, taxonomy_module, evaluation_module, record_module):
            with open(module.__file__, encoding="utf-8") as module_file:
                source = module_file.read()
            for prefix in forbidden_prefixes:
                self.assertNotIn(prefix, source)

    def test_classification_models_are_declarative_only(self) -> None:
        record = build_classification_record()

        self.assertNotIn("route", dir(record))
        self.assertNotIn("invoke", dir(record))
        self.assertNotIn("schedule", dir(record))


if __name__ == "__main__":
    unittest.main()
