import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.knowledge import (
    KnowledgeQuery,
    KnowledgeQueryContract,
    KnowledgeType,
    QueryConstraint,
    QueryMetadata,
    QueryType,
    UniversalKnowledge,
    validate_knowledge_query,
    validate_knowledge_query_contract,
    validate_query_constraint,
    validate_query_metadata,
)
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult


class KnowledgeQueryContractTest(unittest.TestCase):
    def build_constraint(self) -> QueryConstraint:
        return QueryConstraint(
            constraint_type="category",
            operator="equals",
            value="factual",
            constraint_metadata=QueryMetadata(values={"z": "last", "a": "first"}),
        )

    def build_query(self) -> KnowledgeQuery:
        return KnowledgeQuery(
            query_type=QueryType.CATEGORY,
            constraints=(self.build_constraint(),),
            metadata=QueryMetadata(values={"intent": "describe"}),
        )

    def build_contract(self) -> KnowledgeQueryContract:
        return KnowledgeQueryContract(
            supported_query_types=(
                QueryType.EXACT_IDENTIFIER,
                QueryType.CATEGORY,
                QueryType.CLASSIFICATION,
                QueryType.PROVENANCE,
                QueryType.EVIDENCE,
                QueryType.METADATA,
            ),
            supported_constraint_types=(
                "identifier",
                "category",
                "classification",
                "provenance",
                "evidence",
                "metadata",
            ),
            metadata=QueryMetadata(values={"mission": "echo"}),
            contract_version="1.0",
        )

    def test_query_type_values_describe_intent_only(self) -> None:
        self.assertEqual(
            {query_type.value for query_type in QueryType},
            {
                "exact_identifier",
                "category",
                "classification",
                "provenance",
                "evidence",
                "metadata",
            },
        )

    def test_query_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = QueryMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_query_constraint_constructs_deterministic_payload(self) -> None:
        constraint = self.build_constraint()

        self.assertEqual(
            constraint.to_dict(),
            {
                "constraint_type": "category",
                "operator": "equals",
                "value": "factual",
                "constraint_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            constraint.operator = "contains"

    def test_knowledge_query_constructs_deterministic_payload(self) -> None:
        query = self.build_query()

        self.assertEqual(
            query.to_dict(),
            {
                "query_type": "category",
                "constraints": [self.build_constraint().to_dict()],
                "metadata": {"intent": "describe"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            query.query_type = QueryType.METADATA

    def test_knowledge_query_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "supported_query_types": [
                    "exact_identifier",
                    "category",
                    "classification",
                    "provenance",
                    "evidence",
                    "metadata",
                ],
                "supported_constraint_types": [
                    "identifier",
                    "category",
                    "classification",
                    "provenance",
                    "evidence",
                    "metadata",
                ],
                "metadata": {"mission": "echo"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_query_metadata(QueryMetadata(), "metadata"),
            ValidationResult,
        )
        self.assertTrue(validate_query_constraint(self.build_constraint()).is_valid)
        self.assertTrue(validate_knowledge_query(self.build_query()).is_valid)
        self.assertTrue(validate_knowledge_query_contract(self.build_contract()).is_valid)

    def test_validation_reports_invalid_constraint_shape(self) -> None:
        constraint = self.build_constraint()
        object.__setattr__(constraint, "constraint_type", "")
        object.__setattr__(constraint, "operator", "")

        result = validate_query_constraint(constraint)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"constraint.constraint_type", "constraint.operator"},
        )

    def test_validation_reports_invalid_query_shape(self) -> None:
        query = self.build_query()
        object.__setattr__(query, "query_type", "category")
        object.__setattr__(query, "constraints", ("category",))

        result = validate_knowledge_query(query)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"query.query_type", "query.constraints[0]"},
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "supported_query_types", ("category",))
        object.__setattr__(contract, "supported_constraint_types", ("",))

        result = validate_knowledge_query_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "query_contract.contract_version",
                "query_contract.supported_query_types[0]",
                "query_contract.supported_constraint_types[0]",
            },
        )

    def test_universal_knowledge_compatibility_is_preserved(self) -> None:
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000701"),
            knowledge_type=KnowledgeType.FACT,
        )
        query = self.build_query()

        self.assertTrue(knowledge.validate().is_valid)
        self.assertEqual(knowledge.to_dict()["knowledge_type"], "fact")
        self.assertEqual(query.query_type, QueryType.CATEGORY)

    def test_platform_core_serializer_remains_unchanged(self) -> None:
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000702"),
            knowledge_type=KnowledgeType.CONCEPT,
        )

        payload = ObjectSerializer.serialize(knowledge)

        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertNotIn("query", payload)
        self.assertNotIn("query_contract", payload)

    def test_memory_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000703"),
            memory_type=MemoryType.SEMANTIC,
            content="Query contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-echo"),
        )
        contract = self.build_contract()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(validate_knowledge_query_contract(contract).is_valid)

    def test_no_query_execution_or_future_behavior_is_exposed(self) -> None:
        query = self.build_query()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "execute",
            "filter",
            "infer",
            "persist",
            "rank",
            "reason",
            "retrieve",
            "search",
            "semantic_lookup",
            "semantic_search",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(query))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
