import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


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
    xclouds_url = f"http://selenium.xclouds.dev/wd/hub?api_key={api_key}"

    driver = None
    try:
        driver = webdriver.Remote(
            command_executor=xclouds_url,
            options=ChromeOptions(),
        )
        driver.get(TARGET_URL)
        title = driver.title
        if EXPECTED_TITLE not in title:
            raise AssertionError(
                f"Expected title to contain {EXPECTED_TITLE!r}, got {title!r}"
            )
    finally:
        if driver is not None:
            driver.quit()

    print("xClouds Selenium smoke test passed")


if __name__ == "__main__":
    main()
