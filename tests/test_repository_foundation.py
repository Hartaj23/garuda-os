"""Repository foundation tests for GAR-SPRINT-0001 Task 1."""

import unittest

from scripts.validate_repository_foundation import (
    directories_without_readme,
    missing_required_directories,
    missing_required_files,
)


class RepositoryFoundationTest(unittest.TestCase):
    def test_required_repository_files_exist(self) -> None:
        self.assertEqual(missing_required_files(), [])

    def test_required_repository_directories_exist(self) -> None:
        self.assertEqual(missing_required_directories(), [])

    def test_required_directories_have_readmes(self) -> None:
        self.assertEqual(directories_without_readme(), [])


if __name__ == "__main__":
    unittest.main()
