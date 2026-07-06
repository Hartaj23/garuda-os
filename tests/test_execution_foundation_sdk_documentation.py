import unittest
from pathlib import Path

from packages import execution


ROOT = Path(__file__).resolve().parents[1]
SDK_ROOT = ROOT / "docs" / "sdk" / "execution-foundation"

REQUIRED_SDK_FILES = (
    "README.md",
    "execution-sdk-guide.md",
    "developer-guide.md",
    "architecture-guide.md",
    "api-reference.md",
    "best-practices.md",
    "extension-guide.md",
    "practical-examples.md",
)


class ExecutionFoundationSdkDocumentationTest(unittest.TestCase):
    def test_required_sdk_documentation_files_exist(self) -> None:
        for filename in REQUIRED_SDK_FILES:
            with self.subTest(filename=filename):
                self.assertTrue((SDK_ROOT / filename).is_file())

    def test_api_reference_documents_public_exports(self) -> None:
        api_reference = (SDK_ROOT / "api-reference.md").read_text(encoding="utf-8")

        for symbol in execution.__all__:
            with self.subTest(symbol=symbol):
                self.assertIn(symbol, api_reference)

    def test_sdk_documentation_describes_platform_boundary(self) -> None:
        readme = (SDK_ROOT / "README.md").read_text(encoding="utf-8")
        extension_guide = (SDK_ROOT / "extension-guide.md").read_text(encoding="utf-8")

        self.assertIn("Platform Boundary", readme)
        self.assertIn("Out-Of-Scope Extensions", extension_guide)
        self.assertIn("execution behavior", extension_guide)

    def test_sdk_examples_reference_implemented_package(self) -> None:
        practical_examples = (SDK_ROOT / "practical-examples.md").read_text(encoding="utf-8")

        self.assertIn("packages.execution", practical_examples)
        self.assertIn("UniversalExecution", practical_examples)
        self.assertIn("ExecutionWorkspace", practical_examples)


if __name__ == "__main__":
    unittest.main()
