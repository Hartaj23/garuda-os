import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.context import (
    CompositionType,
    ContextComposition,
    ContextScope,
    ContextScopeType,
    ContextSelectionContract,
    ContextSelectionRequest,
    ContextSource,
    ContextSourceType,
    ContextType,
    SelectionCriterion,
    SelectionMetadata,
    SelectionType,
    UniversalContext,
    validate_context_selection_contract,
    validate_context_selection_request,
    validate_selection_criterion,
    validate_selection_metadata,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult


class ContextSelectionContractTest(unittest.TestCase):
    def build_criterion(self) -> SelectionCriterion:
        return SelectionCriterion(
            criterion_name="context_identifier",
            operator="equals",
            criterion_value="context:00000000-0000-0000-0000-000000003001",
        )

    def build_request(self) -> ContextSelectionRequest:
        return ContextSelectionRequest(
            selection_type=SelectionType.EXACT_IDENTIFIER,
            criteria=(self.build_criterion(),),
            metadata=SelectionMetadata(values={"z": "last", "a": "first"}),
        )

    def build_contract(self) -> ContextSelectionContract:
        return ContextSelectionContract(
            supported_selection_types=(
                SelectionType.EXACT_IDENTIFIER,
                SelectionType.SOURCE_BASED,
                SelectionType.SCOPE_BASED,
                SelectionType.TYPE_BASED,
                SelectionType.COMPOSITION_BASED,
            ),
            supported_criteria=(
                "context_identifier",
                "source_identifier",
                "scope_identifier",
                "context_type",
                "composition_identifier",
            ),
            metadata=SelectionMetadata(values={"mission": "echo"}),
            contract_version="1.0",
        )

    def test_selection_type_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {selection_type.value for selection_type in SelectionType},
            {
                "exact_identifier",
                "source_based",
                "scope_based",
                "type_based",
                "composition_based",
            },
        )

    def test_selection_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = SelectionMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_selection_criterion_constructs_deterministic_payload(self) -> None:
        criterion = self.build_criterion()

        self.assertEqual(
            criterion.to_dict(),
            {
                "criterion_name": "context_identifier",
                "operator": "equals",
                "criterion_value": "context:00000000-0000-0000-0000-000000003001",
            },
        )
        with self.assertRaises(FrozenInstanceError):
            criterion.operator = "contains"

    def test_context_selection_request_constructs_deterministic_payload(self) -> None:
        request = self.build_request()

        self.assertEqual(
            request.to_dict(),
            {
                "selection_type": "exact_identifier",
                "criteria": [self.build_criterion().to_dict()],
                "metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            request.selection_type = SelectionType.SOURCE_BASED

    def test_context_selection_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "supported_selection_types": [
                    "exact_identifier",
                    "source_based",
                    "scope_based",
                    "type_based",
                    "composition_based",
                ],
                "supported_criteria": [
                    "context_identifier",
                    "source_identifier",
                    "scope_identifier",
                    "context_type",
                    "composition_identifier",
                ],
                "metadata": {"mission": "echo"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_selection_metadata(SelectionMetadata()),
            ValidationResult,
        )
        self.assertTrue(validate_selection_criterion(self.build_criterion()).is_valid)
        self.assertTrue(validate_context_selection_request(self.build_request()).is_valid)
        self.assertTrue(validate_context_selection_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_criterion_shape(self) -> None:
        criterion = self.build_criterion()
        object.__setattr__(criterion, "criterion_name", "")
        object.__setattr__(criterion, "operator", "")

        result = validate_selection_criterion(criterion)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"criterion.criterion_name", "criterion.operator"},
        )

    def test_validation_reports_invalid_request_shape(self) -> None:
        request = self.build_request()
        object.__setattr__(request, "selection_type", "exact_identifier")
        object.__setattr__(request, "criteria", ("context_identifier",))
        object.__setattr__(request, "metadata", {"bad": "mutable"})

        result = validate_context_selection_request(request)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "selection_request.selection_type",
                "selection_request.criteria[0]",
                "selection_request.metadata",
            },
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "supported_selection_types", ("exact_identifier",))
        object.__setattr__(contract, "supported_criteria", ("",))
        object.__setattr__(contract, "metadata", {"bad": "mutable"})

        result = validate_context_selection_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "selection_contract.contract_version",
                "selection_contract.supported_selection_types[0]",
                "selection_contract.supported_criteria[0]",
                "selection_contract.metadata",
            },
        )

    def test_universal_context_source_scope_and_composition_compatibility(self) -> None:
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000003002"),
            context_type=ContextType.ANALYTICAL,
            context_source=ContextSource(
                source_type=ContextSourceType.KNOWLEDGE,
                source_identifier="knowledge:00000000-0000-0000-0000-000000003101",
            ),
            context_scope=ContextScope(
                scope_type=ContextScopeType.TASK,
                boundary_identifier="task:mission-echo",
            ),
        )
        composition = ContextComposition(
            composition_type=CompositionType.GROUPED,
            context_identifiers=(str(context.object_id),),
        )
        request = ContextSelectionRequest(
            selection_type=SelectionType.COMPOSITION_BASED,
            criteria=(
                SelectionCriterion(
                    criterion_name="composition_identifier",
                    operator="equals",
                    criterion_value="composition:mission-echo",
                ),
            ),
        )

        self.assertTrue(context.validate().is_valid)
        self.assertEqual(composition.context_identifiers, (str(context.object_id),))
        self.assertTrue(validate_context_selection_request(request).is_valid)

    def test_platform_core_serializer_remains_unchanged(self) -> None:
        context = UniversalContext(
            object_id=UUID("00000000-0000-0000-0000-000000003003"),
            context_type=ContextType.CONVERSATIONAL,
        )

        payload = ObjectSerializer.serialize(context)

        self.assertEqual(payload["object_type"], "UniversalContext")
        self.assertNotIn("selection", payload)
        self.assertNotIn("selection_contract", payload)

    def test_memory_and_knowledge_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000003004"),
            memory_type=MemoryType.SEMANTIC,
            content="Selection contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-echo"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000003005"),
            knowledge_type=KnowledgeType.FACT,
        )
        request = ContextSelectionRequest(
            selection_type=SelectionType.SOURCE_BASED,
            criteria=(
                SelectionCriterion(
                    criterion_name="source_identifier",
                    operator="equals",
                    criterion_value=str(memory.object_id),
                ),
                SelectionCriterion(
                    criterion_name="knowledge_identifier",
                    operator="equals",
                    criterion_value=str(knowledge.object_id),
                ),
            ),
        )

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(validate_context_selection_request(request).is_valid)

    def test_no_selection_execution_or_future_behavior_is_exposed(self) -> None:
        request = self.build_request()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "assemble",
            "execute",
            "filter",
            "infer",
            "persist",
            "prioritize",
            "rank",
            "reason",
            "resolve",
            "retrieve",
            "search",
            "select",
            "semantic_lookup",
            "semantic_search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(request))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
