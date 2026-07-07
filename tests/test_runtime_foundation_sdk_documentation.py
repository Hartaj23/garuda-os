import re
import unittest
from pathlib import Path

from packages import runtime


ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "docs" / "sdk" / "runtime"

REQUIRED_SDK_FILES = (
    "README.md",
    "runtime-sdk-guide.md",
    "developer-guide.md",
    "architecture-guide.md",
    "api-reference.md",
    "best-practices.md",
    "extension-guide.md",
    "practical-examples.md",
    "tripartite-distinction-guide.md",
)

PROVENANCE_MARKERS = (
    "Governing Constitution",
    "Governing ADR",
    "Governing Sprint",
    "Repository baseline",
    "c0e6433",
)

FORBIDDEN_SPECULATIVE_TERMS = (
    "future sprint",
    "will be implemented",
    "coming soon",
    "roadmap",
    "REST API",
    "OpenAI",
    "MCP",
)

API_REFERENCE_HEADING_PATTERN = re.compile(r"^### `([A-Za-z_][A-Za-z0-9_]*)`", re.MULTILINE)
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class RuntimeFoundationSdkDocumentationTest(unittest.TestCase):
    def test_required_sdk_documentation_files_exist(self) -> None:
        for filename in REQUIRED_SDK_FILES:
            with self.subTest(filename=filename):
                self.assertTrue((SDK_ROOT / filename).is_file())

    def test_provenance_blocks_present_in_all_sdk_documents(self) -> None:
        for filename in REQUIRED_SDK_FILES:
            with self.subTest(filename=filename):
                content = (SDK_ROOT / filename).read_text(encoding="utf-8")
                for marker in PROVENANCE_MARKERS:
                    self.assertIn(marker, content)

    def test_api_reference_documents_all_public_exports(self) -> None:
        api_reference = (SDK_ROOT / "api-reference.md").read_text(encoding="utf-8")

        for symbol in runtime.__all__:
            with self.subTest(symbol=symbol):
                self.assertIn(symbol, api_reference)

    def test_api_reference_contains_no_undocumented_public_symbols(self) -> None:
        api_reference = (SDK_ROOT / "api-reference.md").read_text(encoding="utf-8")
        documented_symbols = set(API_REFERENCE_HEADING_PATTERN.findall(api_reference))
        public_exports = set(runtime.__all__)

        undocumented = documented_symbols - public_exports
        self.assertEqual(undocumented, set())

    def test_no_undocumented_public_exports_exist(self) -> None:
        api_reference = (SDK_ROOT / "api-reference.md").read_text(encoding="utf-8")
        documented_symbols = set(API_REFERENCE_HEADING_PATTERN.findall(api_reference))
        missing = set(runtime.__all__) - documented_symbols

        self.assertEqual(missing, set())

    def test_api_reference_uses_subsystem_groupings(self) -> None:
        api_reference = (SDK_ROOT / "api-reference.md").read_text(encoding="utf-8")

        for heading in (
            "## Foundation Core",
            "## Runtime Contracts",
            "## Lifecycle and Boundary",
            "## Classification",
            "## Validation",
            "## Registry",
        ):
            self.assertIn(heading, api_reference)

    def test_tripartite_distinction_guide_documents_three_concepts(self) -> None:
        tripartite = (SDK_ROOT / "tripartite-distinction-guide.md").read_text(encoding="utf-8")

        self.assertIn("External Runtime Governance", tripartite)
        self.assertIn("Operational Runtime", tripartite)
        self.assertIn("Universal Execution Foundation", tripartite)

    def test_sdk_documentation_describes_platform_boundary(self) -> None:
        readme = (SDK_ROOT / "README.md").read_text(encoding="utf-8")
        extension_guide = (SDK_ROOT / "extension-guide.md").read_text(encoding="utf-8")

        self.assertIn("Platform Boundary", readme)
        self.assertIn("Out-Of-Scope Extensions", extension_guide)
        self.assertIn("operational runtime", extension_guide)

    def test_sdk_examples_reference_implemented_package(self) -> None:
        practical_examples = (SDK_ROOT / "practical-examples.md").read_text(encoding="utf-8")

        self.assertIn("packages.runtime", practical_examples)
        self.assertIn("CanonicalRuntimeContract", practical_examples)
        self.assertIn("RuntimeRegistry", practical_examples)
        self.assertIn("evaluate_runtime_artifact", practical_examples)

    def test_sdk_examples_include_traceability_metadata(self) -> None:
        practical_examples = (SDK_ROOT / "practical-examples.md").read_text(encoding="utf-8")

        self.assertIn("Referenced symbols", practical_examples)
        self.assertIn("Related mission(s)", practical_examples)
        self.assertIn("Related certification scenario(s)", practical_examples)

    def test_extension_guide_documents_constitutional_workflow(self) -> None:
        extension_guide = (SDK_ROOT / "extension-guide.md").read_text(encoding="utf-8")

        self.assertIn("Constitution (GAR-0019)", extension_guide)
        self.assertIn("Certification (Mission Golf pattern)", extension_guide)

    def test_sdk_documentation_excludes_speculative_capability_language(self) -> None:
        for filename in REQUIRED_SDK_FILES:
            with self.subTest(filename=filename):
                content = (SDK_ROOT / filename).read_text(encoding="utf-8").lower()
                for term in FORBIDDEN_SPECULATIVE_TERMS:
                    self.assertNotIn(term, content)

    def test_cross_references_resolve_correctly(self) -> None:
        for filename in REQUIRED_SDK_FILES:
            sdk_file = SDK_ROOT / filename
            content = sdk_file.read_text(encoding="utf-8")
            for link_target in MARKDOWN_LINK_PATTERN.findall(content):
                if link_target.startswith("http"):
                    continue
                resolved = (sdk_file.parent / link_target).resolve()
                with self.subTest(filename=filename, link_target=link_target):
                    self.assertTrue(resolved.is_file(), f"missing target: {resolved}")

    def test_practical_examples_have_unique_section_headings(self) -> None:
        practical_examples = (SDK_ROOT / "practical-examples.md").read_text(encoding="utf-8")
        headings = re.findall(r"^## (.+)$", practical_examples, re.MULTILINE)

        self.assertEqual(len(headings), len(set(headings)))

    def test_readme_indexes_all_sdk_guides(self) -> None:
        readme = (SDK_ROOT / "README.md").read_text(encoding="utf-8")

        for filename in REQUIRED_SDK_FILES:
            if filename == "README.md":
                continue
            self.assertIn(filename.replace(".md", ""), readme)


if __name__ == "__main__":
    unittest.main()
