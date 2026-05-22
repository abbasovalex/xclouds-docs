#!/usr/bin/env python3
"""Pass a cookie to httpbin through a CDP browser and print the echoed JSON."""

from __future__ import annotations

import argparse
import json
import os
import time

from playwright.sync_api import sync_playwright


COOKIE_NAME = "session_id"
COOKIE_VALUE = "demo-cookie-value"
HTTPBIN_COOKIES = "https://httpbin.org/cookies"
MAX_ATTEMPTS = 3
TIMEOUT_MS = 30_000


def cdp_endpoint() -> str | None:
    explicit_endpoint = (
        os.getenv("XCLOUDS_CDP_WS_ENDPOINT")
        or os.getenv("PUPPETEER_CDP_URL")
    )
    if explicit_endpoint:
        return explicit_endpoint

    api_key = os.getenv("XCLOUDS_CDP_API_KEY") or os.getenv("XCLOUDS_API_KEY")
    if api_key:
        return f"wss://cdp.xclouds.dev/cdp/?api_key={api_key}"

    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        action="store_true",
        help="run with a local Chromium instead of xClouds CDP",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    with sync_playwright() as p:
        if args.local:
            browser = p.chromium.launch(headless=True)
        else:
            endpoint = cdp_endpoint()
            if not endpoint:
                raise SystemExit(
                    "Set XCLOUDS_CDP_WS_ENDPOINT, XCLOUDS_CDP_API_KEY, or XCLOUDS_API_KEY. "
                    "For a local smoke test, run with --local."
                )
            browser = p.chromium.connect_over_cdp(endpoint, timeout=TIMEOUT_MS)

        try:
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            context.add_cookies([{
                "name": COOKIE_NAME,
                "value": COOKIE_VALUE,
                "domain": "httpbin.org",
                "path": "/",
            }])

            page = context.new_page()
            for attempt in range(1, MAX_ATTEMPTS + 1):
                page.goto(HTTPBIN_COOKIES, timeout=TIMEOUT_MS)
                body = page.text_content("body")
                try:
                    data = json.loads(body or "{}")
                    break
                except json.JSONDecodeError:
                    if attempt == MAX_ATTEMPTS:
                        raise RuntimeError(f"Expected JSON from httpbin, got: {body!r}")
                    time.sleep(1)

            assert data["cookies"][COOKIE_NAME] == COOKIE_VALUE
            print(json.dumps(data, indent=2, ensure_ascii=False))
        finally:
            browser.close()


if __name__ == "__main__":
    main()
