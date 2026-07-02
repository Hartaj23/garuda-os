"""Toolchain foundation tests for GAR-SPRINT-0001 Mission Bravo."""

import unittest

from scripts.validate_toolchain import (
    forbidden_paths_present,
    missing_required_files,
    node_tooling_configured,
    python_tooling_configured,
)


class ToolchainFoundationTest(unittest.TestCase):
    def test_required_toolchain_files_exist(self) -> None:
        self.assertEqual(missing_required_files(), [])

    def test_python_tooling_is_configured(self) -> None:
        self.assertTrue(python_tooling_configured())

    def test_node_tooling_is_configured(self) -> None:
        self.assertTrue(node_tooling_configured())

    def test_no_future_sprint_application_paths_exist(self) -> None:
        self.assertEqual(forbidden_paths_present(), [])


if __name__ == "__main__":
    unittest.main()
