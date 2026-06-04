#!/usr/bin/env python3
"""Check that cookie example files match the documentation snippets."""

from __future__ import annotations

import re
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "ru" / "cookbook" / "pass_cookies.md"
ENV_PATH = ROOT.parent / ".env"
SCRIPT_DIR = Path(__file__).resolve().parent
JS_SCRIPT_DIR = SCRIPT_DIR.parent / "js"
EXPECTED_COOKIE = "demo-cookie-value"


EXAMPLES = {
    "Selenium": ("python", SCRIPT_DIR / "pass_cookies_selenium_example.py"),
    "Playwright": ("javascript", JS_SCRIPT_DIR / "pass_cookies_playwright_example.js"),
    "Puppeteer": ("javascript", JS_SCRIPT_DIR / "pass_cookies_puppeteer_example.js"),
}

RUN_EXAMPLES = {
    "Selenium": {
        "env": "SELENIUM_URL",
        "runner": "python",
        "suffix": ".py",
        "package": None,
    },
    "Playwright": {
        "env": "PLAYWRIGHT_URL",
        "runner": "node",
        "suffix": ".mjs",
        "package": "playwright",
    },
    "Puppeteer": {
        "env": "PUPPETEER_CDP_URL",
        "runner": "node",
        "suffix": ".mjs",
        "package": "puppeteer",
    },
}


def section(markdown: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, markdown, flags=re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Section not found: {heading}")
    return match.group("body")


def first_included_code(markdown: str, language: str, base_dir: Path) -> str:
    pattern = rf"\[[^\]]+\]\((?P<path>[^)'\s]+)\s+'?:include\s+:type=code\s+{re.escape(language)}'?\)"
    match = re.search(pattern, markdown)
    if not match:
        raise AssertionError(f"Included code file not found: {language}")

    include_path = (base_dir / match.group("path")).resolve()
    if not include_path.is_file():
        raise AssertionError(f"Included code file is missing: {include_path}")

    return include_path.read_text(encoding="utf-8")


def load_env(path: Path) -> dict[str, str]:
    values = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"').strip("'")
    return values


def api_key_from_url(url: str) -> str:
    query = parse_qs(urlsplit(url).query)
    api_keys = query.get("api_key")
    if not api_keys or not api_keys[0]:
        raise AssertionError("api_key is missing in .env endpoint URL")
    return api_keys[0]


def sanitize(text: str, secrets: list[str]) -> str:
    clean = text
    for secret in secrets:
        if secret:
            clean = clean.replace(secret, "***REDACTED***")
    return clean


def json_from_output(output: str) -> dict:
    stripped = output.strip()
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        match = re.search(r'\{\s*"cookies"\s*:\s*\{.*?\}\s*\}', stripped, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def node_package_available(package: str) -> bool:
    probe = subprocess.run(
        ["node", "--input-type=module", "-e", f"import('{package}')"],
        cwd=ROOT.parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=20,
    )
    return probe.returncode == 0


def run_example(example_path: Path, runner: str, suffix: str, api_key: str) -> subprocess.CompletedProcess[str]:
    code = example_path.read_text(encoding="utf-8").replace("YOUR_API_KEY", api_key)
    with tempfile.NamedTemporaryFile(
        "w",
        suffix=suffix,
        encoding="utf-8",
        dir=ROOT.parent,
        delete=False,
    ) as tmp:
        tmp.write(code)
        tmp_path = Path(tmp.name)

    try:
        return subprocess.run(
            [runner, str(tmp_path)],
            cwd=ROOT.parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60,
        )
    finally:
        tmp_path.unlink(missing_ok=True)


class CookieExampleTests(unittest.TestCase):
    def test_examples_match_documentation(self) -> None:
        markdown = DOC_PATH.read_text(encoding="utf-8")

        for heading, (language, example_path) in EXAMPLES.items():
            with self.subTest(example=heading):
                expected = first_included_code(section(markdown, heading), language, DOC_PATH.parent)
                actual = example_path.read_text(encoding="utf-8")
                self.assertEqual(expected, actual)

    def test_examples_run_with_env_api_keys(self) -> None:
        env = load_env(ENV_PATH)

        for heading, config in RUN_EXAMPLES.items():
            with self.subTest(example=heading):
                endpoint = env.get(config["env"])
                if not endpoint:
                    self.fail(f"{config['env']} is missing in {ENV_PATH}")

                package = config["package"]
                if package and not node_package_available(package):
                    self.skipTest(f"Node package is not installed: {package}")

                api_key = api_key_from_url(endpoint)
                _, example_path = EXAMPLES[heading]
                result = run_example(
                    example_path,
                    config["runner"],
                    config["suffix"],
                    api_key,
                )

                stdout = sanitize(result.stdout, [api_key])
                stderr = sanitize(result.stderr, [api_key])
                self.assertEqual(
                    result.returncode,
                    0,
                    f"{heading} example failed\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}",
                )

                data = json_from_output(result.stdout)
                self.assertEqual(data["cookies"]["session_id"], EXPECTED_COOKIE)


if __name__ == "__main__":
    unittest.main()
