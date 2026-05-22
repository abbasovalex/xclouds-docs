#!/usr/bin/env python3
"""Pass a cookie to httpbin with Selenium and print the echoed JSON."""

from __future__ import annotations

import argparse
import json
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


COOKIE_NAME = "session_id"
COOKIE_VALUE = "demo-cookie-value"
HTTPBIN_HOME = "https://httpbin.org"
HTTPBIN_COOKIES = "https://httpbin.org/cookies"


def selenium_url() -> str | None:
    explicit_url = os.getenv("XCLOUDS_SELENIUM_URL") or os.getenv("SELENIUM_URL")
    if explicit_url:
        return explicit_url

    api_key = os.getenv("XCLOUDS_SELENIUM_API_KEY") or os.getenv("XCLOUDS_API_KEY")
    if api_key:
        return f"http://selenium.xclouds.dev/wd/hub?api_key={api_key}"

    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        action="store_true",
        help="run with a local Chrome instead of xClouds",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    options = ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")

    if args.local:
        driver = webdriver.Chrome(options=options)
    else:
        remote_url = selenium_url()
        if not remote_url:
            raise SystemExit(
                "Set XCLOUDS_SELENIUM_URL, SELENIUM_URL, XCLOUDS_SELENIUM_API_KEY, "
                "or XCLOUDS_API_KEY. For a local smoke test, run with --local."
            )
        driver = webdriver.Remote(command_executor=remote_url, options=options)

    try:
        driver.get(HTTPBIN_HOME)
        driver.add_cookie({
            "name": COOKIE_NAME,
            "value": COOKIE_VALUE,
            "path": "/",
        })

        driver.get(HTTPBIN_COOKIES)
        body = driver.find_element("tag name", "pre").text
        data = json.loads(body)

        assert data["cookies"][COOKIE_NAME] == COOKIE_VALUE
        print(json.dumps(data, indent=2, ensure_ascii=False))
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
