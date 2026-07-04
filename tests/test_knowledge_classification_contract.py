import unittest
from dataclasses import FrozenInstanceError
from uuid import UUID

from packages.knowledge import (
    ClassificationDescriptor,
    ClassificationDimension,
    ClassificationMetadata,
    KnowledgeCategory,
    KnowledgeClassificationContract,
    KnowledgeType,
    UniversalKnowledge,
    validate_classification_descriptor,
    validate_classification_dimension,
    validate_classification_metadata,
    validate_knowledge_classification_contract,
)
from packages.memory import MemorySource, MemoryType, UniversalMemory
from packages.objects import ObjectSerializer, ValidationResult


class KnowledgeClassificationContractTest(unittest.TestCase):
    def build_dimension(self) -> ClassificationDimension:
        return ClassificationDimension(
            dimension_name="domain",
            dimension_value="finance",
            dimension_metadata=ClassificationMetadata(values={"z": "last", "a": "first"}),
        )

    def build_descriptor(self) -> ClassificationDescriptor:
        return ClassificationDescriptor(
            category=KnowledgeCategory.FACTUAL,
            dimensions=(self.build_dimension(),),
            classification_metadata=ClassificationMetadata(values={"source": "contract"}),
        )

    def build_contract(self) -> KnowledgeClassificationContract:
        return KnowledgeClassificationContract(
            supported_categories=(
                KnowledgeCategory.FACTUAL,
                KnowledgeCategory.CONCEPTUAL,
                KnowledgeCategory.PROCEDURAL,
            ),
            supported_dimensions=(
                ClassificationDimension(dimension_name="domain"),
                ClassificationDimension(dimension_name="abstraction_level"),
                ClassificationDimension(dimension_name="permanence"),
                ClassificationDimension(dimension_name="source_category"),
            ),
            metadata=ClassificationMetadata(values={"mission": "delta"}),
            contract_version="1.0",
        )

    def test_knowledge_category_values_are_descriptive_only(self) -> None:
        self.assertEqual(
            {category.value for category in KnowledgeCategory},
            {
                "factual",
                "conceptual",
                "procedural",
                "structural",
                "observational",
            },
        )

    def test_classification_metadata_is_immutable_and_deterministic(self) -> None:
        metadata = ClassificationMetadata(values={"z": "last", "a": "first"})

        self.assertEqual(metadata.to_dict(), {"a": "first", "z": "last"})
        with self.assertRaises(FrozenInstanceError):
            metadata.values = ()

    def test_classification_dimension_constructs_deterministic_payload(self) -> None:
        dimension = self.build_dimension()

        self.assertEqual(
            dimension.to_dict(),
            {
                "dimension_name": "domain",
                "dimension_value": "finance",
                "dimension_metadata": {"a": "first", "z": "last"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            dimension.dimension_name = "source_category"

    def test_classification_descriptor_constructs_deterministic_payload(self) -> None:
        descriptor = self.build_descriptor()

        self.assertEqual(
            descriptor.to_dict(),
            {
                "category": "factual",
                "dimensions": [self.build_dimension().to_dict()],
                "classification_metadata": {"source": "contract"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            descriptor.category = KnowledgeCategory.CONCEPTUAL

    def test_knowledge_classification_contract_constructs_deterministic_payload(self) -> None:
        contract = self.build_contract()

        self.assertEqual(contract.to_dict(), contract.to_dict())
        self.assertEqual(
            contract.to_dict(),
            {
                "contract_version": "1.0",
                "supported_categories": ["factual", "conceptual", "procedural"],
                "supported_dimensions": [
                    {
                        "dimension_name": "domain",
                        "dimension_value": None,
                        "dimension_metadata": {},
                    },
                    {
                        "dimension_name": "abstraction_level",
                        "dimension_value": None,
                        "dimension_metadata": {},
                    },
                    {
                        "dimension_name": "permanence",
                        "dimension_value": None,
                        "dimension_metadata": {},
                    },
                    {
                        "dimension_name": "source_category",
                        "dimension_value": None,
                        "dimension_metadata": {},
                    },
                ],
                "metadata": {"mission": "delta"},
            },
        )
        with self.assertRaises(FrozenInstanceError):
            contract.contract_version = "2.0"

    def test_validation_helpers_return_platform_validation_results(self) -> None:
        self.assertIsInstance(
            validate_classification_metadata(ClassificationMetadata(), "metadata"),
            ValidationResult,
        )
        self.assertTrue(validate_classification_dimension(self.build_dimension()).is_valid)
        self.assertTrue(validate_classification_descriptor(self.build_descriptor()).is_valid)
        self.assertTrue(
            validate_knowledge_classification_contract(self.build_contract()).is_valid
        )

    def test_validation_reports_invalid_dimension_shape(self) -> None:
        dimension = ClassificationDimension(dimension_name="domain")
        object.__setattr__(dimension, "dimension_name", "")
        object.__setattr__(dimension, "dimension_value", 123)

        result = validate_classification_dimension(dimension)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"dimension.dimension_name", "dimension.dimension_value"},
        )

    def test_validation_reports_invalid_descriptor_shape(self) -> None:
        descriptor = self.build_descriptor()
        object.__setattr__(descriptor, "category", "factual")
        object.__setattr__(descriptor, "dimensions", ("domain",))

        result = validate_classification_descriptor(descriptor)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {"descriptor.category", "descriptor.dimensions[0]"},
        )

    def test_validation_reports_invalid_contract_shape(self) -> None:
        contract = self.build_contract()
        object.__setattr__(contract, "contract_version", "")
        object.__setattr__(contract, "supported_categories", ("factual",))
        object.__setattr__(contract, "supported_dimensions", ("domain",))

        result = validate_knowledge_classification_contract(contract)

        self.assertFalse(result.is_valid)
        self.assertEqual(
            {error.field for error in result.errors},
            {
                "classification_contract.contract_version",
                "classification_contract.supported_categories[0]",
                "classification_contract.supported_dimensions[0]",
            },
        )

    def test_universal_knowledge_compatibility_is_preserved(self) -> None:
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000601"),
            knowledge_type=KnowledgeType.FACT,
        )
        descriptor = self.build_descriptor()

        self.assertTrue(knowledge.validate().is_valid)
        self.assertEqual(knowledge.to_dict()["knowledge_type"], "fact")
        self.assertEqual(descriptor.category, KnowledgeCategory.FACTUAL)

    def test_platform_core_serializer_remains_unchanged(self) -> None:
        knowledge = UniversalKnowledge(
            object_id=UUID("00000000-0000-0000-0000-000000000602"),
            knowledge_type=KnowledgeType.CONCEPT,
        )

        payload = ObjectSerializer.serialize(knowledge)

        self.assertEqual(payload["object_type"], "UniversalKnowledge")
        self.assertNotIn("classification", payload)
        self.assertNotIn("classification_descriptor", payload)

    def test_memory_foundation_compatibility_is_preserved(self) -> None:
        memory = UniversalMemory(
            object_id=UUID("00000000-0000-0000-0000-000000000603"),
            memory_type=MemoryType.SEMANTIC,
            content="Classification contracts coexist with memory.",
            source=MemorySource(source_type="test", source_identifier="mission-delta"),
        )
        contract = self.build_contract()

        self.assertTrue(memory.validate().is_valid)
        self.assertTrue(validate_knowledge_classification_contract(contract).is_valid)

    def test_no_classification_engine_or_future_behavior_is_exposed(self) -> None:
        descriptor = self.build_descriptor()
        contract = self.build_contract()
        forbidden_names = {
            "ai",
            "classify",
            "execute",
            "infer",
            "ontology",
            "persist",
            "query",
            "reason",
            "search",
            "semantic_search",
            "taxonomy",
            "workflow",
        }

        self.assertTrue(forbidden_names.isdisjoint(set(dir(descriptor))))
        self.assertTrue(forbidden_names.isdisjoint(set(dir(contract))))


if __name__ == "__main__":
    unittest.main()
