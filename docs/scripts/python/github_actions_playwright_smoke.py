import os
import sys

from playwright.sync_api import sync_playwright


PLAYWRIGHT_VERSION = "1.58"
TARGET_URL = "https://example.com"
EXPECTED_TITLE = "Example Domain"


def require_api_key() -> str:
    api_key = os.environ.get("XCLOUDS_API_KEY", "").strip()
    if not api_key:
        print("XCLOUDS_API_KEY is not set", file=sys.stderr)
        sys.exit(2)
    return api_key


def main() -> None:
    api_key = require_api_key()
    ws_endpoint = (
        f"wss://playwright.xclouds.dev/v{PLAYWRIGHT_VERSION}/?api_key={api_key}"
    )

    browser = None
    with sync_playwright() as p:
        try:
            browser = p.chromium.connect(ws_endpoint=ws_endpoint)
            page = browser.new_page()
            page.goto(TARGET_URL, wait_until="domcontentloaded")
            title = page.title()
            if EXPECTED_TITLE not in title:
                raise AssertionError(
                    f"Expected title to contain {EXPECTED_TITLE!r}, got {title!r}"
                )
        finally:
            if browser is not None:
                browser.close()

    print("xClouds Playwright smoke test passed")


if __name__ == "__main__":
    main()
