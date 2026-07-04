import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.context import (
    CompositionMetadata,
    CompositionType,
    ContextComposition,
    ContextCompositionContract,
    ContextScope,
    ContextScopeType,
    ContextSource,
    ContextSourceType,
    ContextType,
    UniversalContext,
    validate_composition_metadata,
    validate_context_composition,
    validate_context_composition_contract,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult


class ContextCompositionContractTest(unittest.TestCase):
    def build_composition(self) -> ContextComposition:
        return ContextComposition(
            composition_type=CompositionType.LAYERED,
            context_identifiers=(
                "context:00000000-0000-0000-0000-000000002001",
                "context:00000000-0000-0000-0000-000000002002",
            ),
            composition_metadata=CompositionMetadata(
                values={"z": "last", "a": "first"},
            ),
        )

    def build_contract(self) -> ContextCompositionContract:
        return ContextCompositionContract(
            supported_composition_types=(
                CompositionType.SEQUENTIAL,
                CompositionType.PARALLEL,
                CompositionType.LAYERED,
                CompositionType.HIERARCHICAL,
                CompositionType.GROUPED,
            ),
            supported_metadata=CompositionMetadata(values={"mission": "delta"}),
            contract_version="1.0",
        )

    def test_composition_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {composition_type.value for composition_type in CompositionType},
            {"sequential", "parallel", "layered", "hierarchical", "grouped"},
        )

    def test_composition_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = CompositionMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_context_composition_constructs_deterministic_payload(self) -> None:
        composition = self.build_composition()

        self.assertEqual(
            composition.to_dict(),
            {
                "composition_type": "layered",
                "context_identifiers": [
                    "context:00000000-0000-0000-0000-000000002001",
                    "context:00000000-0000-0000-0000-000000002002",
                ],
                "composition_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            composition.composition_type = CompositionType.GROUPED

    def test_context_composition_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "supported_composition_types": [
                    "sequential",
                    "parallel",
                    "layered",
                    "hierarchical",
                    "grouped",
                ],
                "supported_metadata": {"mission": "delta"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_composition_metadata(CompositionMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_context_composition(self.build_composition()).is_valid)
        self.assertTrue(validate_context_composition_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_composition_shape(self) -> None:
        composition = self.build_composition()
        object.__setattr__(composition, "composition_type", "layered")
        object.__setattr__(composition, "context_identifiers", ("", object()))
        object.__setattr__(composition, "composition_metadata", {"bad": "mutable"})

        result = validate_context_composition(composition)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "context_composition.composition_type",
                "context_composition.context_identifiers[0]",
                "context_composition.context_identifiers[1]",
                "context_composition.composition_metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "supported_composition_types", ("layered",))
        object.__setattr__(contract, "supported_metadata", {"bad": "mutable"})

        result = validate_context_composition_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "composition_contract.contract_version",
                "composition_contract.supported_composition_types[0]",
                "composition_contract.supported_metadata",
            },
        )

    def test_universal_context_compatibility_uses_opaque_identifiers_only(self) -> None:
        first_context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000002003"),
            context_type=ContextType.ANALYTICAL,
            context_source=ContextSource(
                source_type=ContextSourceType.KNOWLEDGE,
                source_identifier="knowledge:00000000-0000-0000-0000-000000002101",
            ),
            context_scope=ContextScope(
                scope_type=ContextScopeType.TASK,
                boundary_identifier="task:mission-delta",
            ),
        )
        second_context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000002004"),
            context_type=ContextType.OPERATIONAL,
        )
        composition = ContextComposition(
            composition_type=CompositionType.SEQUENTIAL,
            context_identifiers=(
                str(first_context.object_id),
                str(second_context.object_id),
            ),
        )

        self.assertTrue(first_context.validate().is_valid)
        self.assertTrue(second_context.validate().is_valid)
        self.assertTrue(validate_context_composition(composition).is_valid)
        self.assertEqual(
            composition.to_dict()["context_identifiers"],
            [
                "00000000-0000-0000-0000-000000002003",
                "00000000-0000-0000-0000-000000002004",
            ],
        )
        self.assertNotIn(first_context, composition.context_identifiers)
        self.assertNotIn(second_context, composition.context_identifiers)

    def test_platform_core_serializer_remains_unchanged(self) -> None:
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000002005"),
            context_type=ContextType.CONVERSATIONAL,
        )

        payload = ObjectSerializer.serialize(context)

        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertNotIn("composition", payload)
        self.assertNotIn("composition_contract", payload)

    def test_memory_and_knowledge_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000002006"),
            memory_type=MemoryType.SEMANTIC,
            content="Composition contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-delta"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000002007"),
            knowledge_type=KnowledgeType.FACT,
        )
        composition = ContextComposition(
            composition_type=CompositionType.GROUPED,
            context_identifiers=(
                f"memory-context:{memory.object_id}",
                f"knowledge-context:{knowledge.object_id}",
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(validate_context_composition(composition).is_valid)

    def test_no_composition_execution_or_future_behavior_is_exposed(self) -> None:
        composition = self.build_composition()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "compose",
            "execute",
            "filter",
            "infer",
            "persist",
            "rank",
            "reason",
            "resolve",
            "retrieve",
            "search",
            "semantic_lookup",
            "semantic_search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(composition))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
