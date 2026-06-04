# Playwright Example

Use this example when you want Playwright to connect to a browser hosted by xClouds.

## Prerequisites

Use a Playwright client version that matches the endpoint version.

```bash
npm install playwright@1.58
```

For Python:

```bash
pip install playwright==1.58
```

## Node.js Connection

[chromium_connect.js](../../code_examples/playwright/javascript/chromium_connect.js ':include :type=code javascript')

## Python Connection

[chromium_connect.py](../../code_examples/playwright/python/chromium_connect.py ':include :type=code python')

## Java Connection

[chromium_connect.java](../../code_examples/playwright/java/chromium_connect.java ':include :type=code java')

Maven dependency:

```xml
<dependency>
  <groupId>com.microsoft.playwright</groupId>
  <artifactId>playwright</artifactId>
  <version>1.58.0</version>
</dependency>
```

## C# Connection

[chromium_connect.cs](../../code_examples/playwright/csharp/chromium_connect.cs ':include :type=code csharp')

Install the matching package:

```bash
dotnet add package Microsoft.Playwright --version 1.58.0
```

## Choose A Browser

Available browser names in the source example are `chromium`, `firefox`, and `webkit`.

### Node.js

[firefox_connect.js](../../code_examples/playwright/javascript/firefox_connect.js ':include :type=code javascript')

### Python

[firefox_connect.py](../../code_examples/playwright/python/firefox_connect.py ':include :type=code python')

### Java

[firefox_connect.java](../../code_examples/playwright/java/firefox_connect.java ':include :type=code java')

### C#

[firefox_connect.cs](../../code_examples/playwright/csharp/firefox_connect.cs ':include :type=code csharp')

## Screenshots And PDFs

### Node.js

[screenshots_pdf.js](../../code_examples/playwright/javascript/screenshots_pdf.js ':include :type=code javascript')

### Python

[screenshots_pdf.py](../../code_examples/playwright/python/screenshots_pdf.py ':include :type=code python')

### Java

[screenshots_pdf.java](../../code_examples/playwright/java/screenshots_pdf.java ':include :type=code java')

### C#

[screenshots_pdf.cs](../../code_examples/playwright/csharp/screenshots_pdf.cs ':include :type=code csharp')

Expected result:

```text
screenshot.png and page.pdf are written in the current directory.
```

## Common Errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Connection is rejected | API key is missing or wrong | Replace `YOUR_API_KEY` with your xClouds Playwright key |
| Protocol error after connect | Client and endpoint versions do not match | Use `playwright@1.58` with `/v1.58/` |
| PDF fails | PDF generation is Chromium-only | Use `chromium.connect(...)` for PDF |
| Browser choice fails | Browser import does not match the browser you connect with | Import `chromium`, `firefox`, or `webkit` explicitly |
| Script exits before work finishes | Missing `await` | Await navigation and file writes before closing |

## Production Notes

Store API keys outside source code. Close the browser after each run, especially in CI and scheduled jobs.
