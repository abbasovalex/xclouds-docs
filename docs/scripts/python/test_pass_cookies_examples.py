#!/usr/bin/env python3
"""Check that cookie example files match the documentation snippets."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "ru" / "cookbook" / "pass_cookies.md"
SCRIPT_DIR = Path(__file__).resolve().parent


EXAMPLES = {
    "Selenium": ("python", SCRIPT_DIR / "pass_cookies_selenium_example.py"),
    "Playwright": ("javascript", SCRIPT_DIR / "pass_cookies_playwright_example.js"),
    "Puppeteer": ("javascript", SCRIPT_DIR / "pass_cookies_puppeteer_example.js"),
}


def section(markdown: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, markdown, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Section not found: {heading}")
    return match.group("body")


def first_code_block(markdown: str, language: str) -> str:
    pattern = rf"```{re.escape(language)}\n(?P<code>.*?)\n```"
    match = re.search(pattern, markdown, flags=re.DOTALL)
    if not match:
        raise AssertionError(f"Code block not found: {language}")
    return match.group("code").rstrip() + "\n"


class CookieExampleTests(unittest.TestCase):
    def test_examples_match_documentation(self) -> None:
        markdown = DOC_PATH.read_text(encoding="utf-8")

        for heading, (language, example_path) in EXAMPLES.items():
            with self.subTest(example=heading):
                expected = first_code_block(section(markdown, heading), language)
                actual = example_path.read_text(encoding="utf-8")
                self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
