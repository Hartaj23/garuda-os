import json
import unittest
from datetime import datetime
from uuid import UUID

from packages.context import (
    CompositionMetadata,
    CompositionType,
    ContextComposition,
    ContextCompositionContract,
    ContextConfidence,
    ContextMetadata,
    ContextScope,
    ContextScopeType,
    ContextSelectionContract,
    ContextSelectionRequest,
    ContextSource,
    ContextSourceType,
    ContextState,
    ContextType,
    ContextWorkspace,
    SelectionCriterion,
    SelectionMetadata,
    SelectionType,
    UniversalContext,
    WorkspaceStatistics,
    validate_context_composition,
    validate_context_composition_contract,
    validate_context_selection_contract,
    validate_context_selection_request,
    validate_context_workspace,
)
from packages.knowledge import KnowledgeType, UniversalKnowledge
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import (
    CanonicalObject,
    LifecycleState,
    ObjectRegistry,
    ObjectSerializer,
    Relationship,
    RelationshipType,
    ValidationResult,
)


TIMESTAMP = datetime.fromisoformat("2026-07-04T00:00:00+00:00")


def build_certified_source() -> ContextSource:
    return ContextSource(
        source_type=ContextSourceType.KNOWLEDGE,
        source_identifier="knowledge:00000000-0000-0000-0000-000000005101",
        created_at=TIMESTAMP,
        source_metadata={"z": "last", "a": "first"},
    )


def build_certified_scope() -> ContextScope:
    return ContextScope(
        scope_type=ContextScopeType.TASK,
        boundary_identifier="task:mission-golf",
        lifetime_metadata={"expires": "manual"},
        scope_metadata={"z": "last", "a": "first"},
    )


def build_certified_context(
    context_id: str = "00000000-0000-0000-0000-000000005001",
) -> UniversalContext:
    return UniversalContext(
        object_id=UUID(context_id),
        context_type=ContextType.ANALYTICAL,
        context_state=ContextState.VALIDATED,
        context_confidence=ContextConfidence(level="high", rationale="certified"),
        context_metadata=ContextMetadata(values={"z": "last", "a": "first"}),
        context_source=build_certified_source(),
        context_scope=build_certified_scope(),
        metadata={"owner": "platform", "mission": "golf"},
        tags=["context", "certification"],
        lifecycle_state=LifecycleState.DRAFT,
        created_by="codex",
        updated_by="codex",
        created_at=TIMESTAMP,
        updated_at=TIMESTAMP,
    )


class ContextPlatformIntegrationCertificationTest(unittest.TestCase):
    def test_scenario_1_universal_context_certification(self) -> None:
        context = build_certified_context()
        payload = context.to_dict()
        encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        registry = ObjectRegistry()
        registry.register(UniversalContext)
        target_id = UUID("00000000-0000-0000-0000-000000005201")
        relationship = Relationship(
            source_object_id=context.object_id,
            target_object_id=target_id,
            relationship_type=RelationshipType.REFERENCES,
        )

        self.assertIsInstance(context, CanonicalObject)
        self.assertIsInstance(context.validate(), ValidationResult)
        self.assertTrue(context.validate().is_valid)
        self.assertEqual(payload, build_certified_context().to_dict())
        self.assertEqual(encoded, json.dumps(payload, sort_keys=True, separators=(",", ":")))
        self.assertEqual(ObjectSerializer.serialize(context)["object_type"], "UniversalContext")
        self.assertEqual(registry.lookup("UniversalContext"), UniversalContext)
        context.transition_to(LifecycleState.ACTIVE)
        self.assertEqual(context.lifecycle_state, LifecycleState.ACTIVE)
        self.assertEqual(relationship.to_dict()["source_object_id"], str(context.object_id))
        self.assertEqual(relationship.to_dict()["relationship_type"], "references")

    def test_scenario_2_context_source_scope_certification(self) -> None:
        source = build_certified_source()
        scope = build_certified_scope()
        context = build_certified_context()

        self.assertEqual(
            source.to_dict(),
            {
                "source_type": "knowledge",
                "source_identifier": "knowledge:00000000-0000-0000-0000-000000005101",
                "created_at": TIMESTAMP.isoformat(),
                "source_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertEqual(
            scope.to_dict(),
            {
                "scope_type": "task",
                "boundary_identifier": "task:mission-golf",
                "lifetime_metadata": {"expires": "manual"},
                "scope_metadata": {"a": "first", "z": "last"},
            },
        )
        self.assertTrue(context.validate().is_valid)
        self.assert_no_behavior(source, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(scope, {"enforce", "filter", "select"})

    def test_scenario_3_context_composition_contract_certification(self) -> None:
        composition = ContextComposition(
            composition_type=CompositionType.LAYERED,
            context_identifiers=(
                "context:00000000-0000-0000-0000-000000005001",
                "context:00000000-0000-0000-0000-000000005002",
            ),
            composition_metadata=CompositionMetadata(values={"z": "last", "a": "first"}),
        )
        contract = ContextCompositionContract(
            supported_composition_types=(
                CompositionType.SEQUENTIAL,
                CompositionType.PARALLEL,
                CompositionType.LAYERED,
            ),
            supported_metadata=CompositionMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_context_composition(composition).is_valid)
        self.assertTrue(validate_context_composition_contract(contract).is_valid)
        self.assertEqual(composition.to_dict(), composition.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            composition.to_dict()["context_identifiers"],
            [
                "context:00000000-0000-0000-0000-000000005001",
                "context:00000000-0000-0000-0000-000000005002",
            ],
        )
        self.assert_no_behavior(composition, {"compose", "execute", "resolve", "search"})
        self.assert_no_behavior(contract, {"compose", "engine", "retrieve", "query"})

    def test_scenario_4_context_selection_contract_certification(self) -> None:
        request = ContextSelectionRequest(
            selection_type=SelectionType.EXACT_IDENTIFIER,
            criteria=(
                SelectionCriterion(
                    criterion_name="context_identifier",
                    operator="equals",
                    criterion_value="00000000-0000-0000-0000-000000005001",
                ),
            ),
            metadata=SelectionMetadata(values={"z": "last", "a": "first"}),
        )
        contract = ContextSelectionContract(
            supported_selection_types=(
                SelectionType.EXACT_IDENTIFIER,
                SelectionType.SOURCE_BASED,
                SelectionType.SCOPE_BASED,
                SelectionType.TYPE_BASED,
                SelectionType.COMPOSITION_BASED,
            ),
            supported_criteria=("context_identifier", "source_identifier", "scope_identifier"),
            metadata=SelectionMetadata(values={"mission": "golf"}),
            contract_version="1.0",
        )

        self.assertTrue(validate_context_selection_request(request).is_valid)
        self.assertTrue(validate_context_selection_contract(contract).is_valid)
        self.assertEqual(request.to_dict(), request.to_dict())
        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assert_no_behavior(request, {"select", "retrieve", "search", "filter", "rank"})
        self.assert_no_behavior(contract, {"execute", "engine", "resolve", "query"})

    def test_scenario_5_context_workspace_certification(self) -> None:
        workspace = ContextWorkspace()
        context = build_certified_context()

        self.assertIsInstance(workspace.statistics(), WorkspaceStatistics)
        workspace.add(context)
        with self.assertRaises(ValueError):
            workspace.add(context)

        self.assertIs(workspace.get(context.object_id), context)
        self.assertIs(workspace.get(str(context.object_id)), context)
        self.assertEqual(workspace.identifiers(), (context.object_id,))
        self.assertEqual(workspace.statistics().total_contexts, 1)
        self.assertIs(workspace.remove(str(context.object_id)), context)
        self.assertIsNone(workspace.get(context.object_id))
        workspace.add(context)
        workspace.clear()
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_contexts, 0)
        self.assertTrue(validate_context_workspace(workspace).is_valid)
        self.assertFalse(hasattr(workspace, "to_dict"))
        self.assert_no_behavior(workspace, {"search", "filter", "rank", "persist", "save"})

    def test_scenario_6_end_to_end_context_foundation_certification(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000005301"),
            memory_type=MemoryType.SEMANTIC,
            content="Context certification coexists with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-golf"),
        )
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000005302"),
            knowledge_type=KnowledgeType.FACT,
        )
        context = build_certified_context()
        composition = ContextComposition(
            composition_type=CompositionType.GROUPED,
            context_identifiers=(str(context.object_id),),
        )
        selection = ContextSelectionRequest(
            selection_type=SelectionType.COMPOSITION_BASED,
            criteria=(
                SelectionCriterion(
                    criterion_name="composition_identifier",
                    operator="equals",
                    criterion_value="composition:mission-golf",
                ),
            ),
        )
        workspace = ContextWorkspace()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(knowledge.validate().is_valid)
        self.assertTrue(context.validate().is_valid)
        self.assertEqual(ObjectSerializer.serialize(context)["object_id"], str(context.object_id))
        self.assertEqual(context.context_source.source_identifier, build_certified_source().source_identifier)
        self.assertEqual(context.context_scope.boundary_identifier, "task:mission-golf")
        self.assertTrue(validate_context_composition(composition).is_valid)
        self.assertTrue(validate_context_selection_request(selection).is_valid)

        workspace.add(context)
        self.assertIs(workspace.get(context.object_id), context)
        self.assertIs(workspace.remove(context.object_id), context)
        self.assertTrue(workspace.validate().is_valid)
        self.assertEqual(workspace.identifiers(), ())
        self.assertEqual(workspace.statistics().total_contexts, 0)

    def test_explicit_context_foundation_boundary_certification(self) -> None:
        source = build_certified_source()
        scope = build_certified_scope()
        composition = ContextComposition(
            composition_type=CompositionType.SEQUENTIAL,
            context_identifiers=("00000000-0000-0000-0000-000000005001",),
        )
        selection = ContextSelectionRequest(
            selection_type=SelectionType.EXACT_IDENTIFIER,
            criteria=(
                SelectionCriterion(
                    criterion_name="context_identifier",
                    operator="equals",
                    criterion_value="00000000-0000-0000-0000-000000005001",
                ),
            ),
        )
        workspace = ContextWorkspace()

        self.assert_no_behavior(source, {"resolve", "retrieve", "search"})
        self.assert_no_behavior(scope, {"enforce", "filter", "select"})
        self.assert_no_behavior(composition, {"compose", "execute", "resolve"})
        self.assert_no_behavior(selection, {"select", "retrieve", "rank", "search"})
        self.assert_no_behavior(workspace, {"persist", "save", "load", "query", "search"})

    def assert_no_behavior(self, obj: object, forbidden_names: set[str]) -> None:
        self.assertTrue(forbidden_names.isdisjoint(set(dir(obj))))


if __name__ == "__main__":
    unittest.main()
