#!/usr/bin/env python3
"""POST JSON to bin.xclouds.dev and verify the echoed payload."""

from __future__ import annotations

import json
import urllib.request


URL = "https://bin.xclouds.dev/post"
PAYLOAD = {
    "source": "xclouds-docs",
    "example": "post-json",
    "message": "hello from a docs script",
}


def main() -> None:
    body = json.dumps(PAYLOAD).encode("utf-8")
    request = urllib.request.Request(
        URL,
        data=body,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "xclouds-docs-example/1.0",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        assert response.status == 200, f"expected HTTP 200, got {response.status}"
        data = json.loads(response.read().decode("utf-8"))

    assert data["json"] == PAYLOAD
    assert data["headers"]["Content-Type"] == "application/json"

    print("POST example passed")


if __name__ == "__main__":
    main()
