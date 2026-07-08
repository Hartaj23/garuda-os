"""Tests for Mission 001 Phase C — Public Foundation Implementation."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEBSITE = ROOT / "website"
PAGES = WEBSITE / "public"
BUILD_SCRIPT = WEBSITE / "scripts" / "build_site.py"


class Mission001PhaseCImplementationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        result = subprocess.run(
            [sys.executable, str(BUILD_SCRIPT)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        cls.build_result = result

    def test_build_succeeds(self) -> None:
        self.assertEqual(
            self.build_result.returncode,
            0,
            msg=self.build_result.stderr or self.build_result.stdout,
        )

    def test_expected_pages_exist(self) -> None:
        expected = [
            PAGES / "index.html",
            PAGES / "about" / "manifesto.html",
            PAGES / "constitutional-engineering.html",
            PAGES / "institution" / "governance.html",
            PAGES / "library" / "book-one.html",
            PAGES / "research.html",
        ]
        for path in expected:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing {path}")

    def test_styles_and_mark_assets_exist(self) -> None:
        self.assertTrue((PAGES / "assets" / "styles" / "main.css").is_file())
        self.assertTrue((PAGES / "assets" / "styles" / "tokens.css").is_file())
        self.assertTrue((PAGES / "assets" / "mark" / "institutional-mark-v1.0.svg").is_file())

    def test_home_page_contains_institutional_mark(self) -> None:
        html = (PAGES / "index.html").read_text(encoding="utf-8")
        self.assertIn('class="site-mark"', html)
        self.assertIn('class="home-proposition"', html)
        self.assertIn("Building institutions worthy of the intelligence they guide.", html)

    def test_manifesto_page_has_repository_callout(self) -> None:
        html = (PAGES / "about" / "manifesto.html").read_text(encoding="utf-8")
        self.assertIn('class="repository-callout"', html)
        self.assertIn("docs/institutional/MANIFESTO.md", html)
        self.assertIn('class="reading-journey"', html)

    def test_css_uses_design_tokens(self) -> None:
        css = (PAGES / "assets" / "styles" / "tokens.css").read_text(encoding="utf-8")
        self.assertIn("--color-background-primary: #F7F5F0", css)
        self.assertIn("--font-size-base: 1.0625rem", css)
        self.assertIn("--layout-max-width-content: 48rem", css)

    def test_repository_links_target_public_docs_mirror(self) -> None:
        html = (PAGES / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="docs/institutional/PUBLIC-WELCOME.md"', html)
        docs_mirror = PAGES / "docs" / "institutional" / "PUBLIC-WELCOME.md"
        self.assertTrue(docs_mirror.is_file())


    def test_semantic_structure(self) -> None:
        html = (PAGES / "index.html").read_text(encoding="utf-8")
        self.assertIn("<header", html)
        self.assertIn("<main", html)
        self.assertIn("<footer", html)
        self.assertIn("<article", html)
        self.assertIn('lang="en"', html)


if __name__ == "__main__":
    unittest.main()
