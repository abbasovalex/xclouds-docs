#!/usr/bin/env python3
"""Check an expected status code from bin.xclouds.dev"""

from __future__ import annotations

import urllib.error
import urllib.request


URL = "https://bin.xclouds.dev/status/204"


def main() -> None:
    request = urllib.request.Request(URL, headers={"User-Agent": "xclouds-docs-example/1.0"})

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code

    assert status == 204, f"expected HTTP 204, got {status}"

    print("Status example passed")


if __name__ == "__main__":
    main()
