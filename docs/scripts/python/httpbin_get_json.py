#!/usr/bin/env python3
"""GET JSON from bin.xclouds.dev and verify the response shape."""

from __future__ import annotations

import json
import urllib.request


URL = "https://bin.xclouds.dev/get?tool=xclouds-docs&example=get-json"


def main() -> None:
    request = urllib.request.Request(URL, headers={"User-Agent": "xclouds-docs-example/1.0"})

    with urllib.request.urlopen(request, timeout=20) as response:
        assert response.status == 200, f"expected HTTP 200, got {response.status}"
        data = json.loads(response.read().decode("utf-8"))

    assert data["args"]["tool"] == "xclouds-docs"
    assert data["args"]["example"] == "get-json"
    assert data["url"].startswith("https://bin.xclouds.dev/get")

    print("GET example passed")


if __name__ == "__main__":
    main()
