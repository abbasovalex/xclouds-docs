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

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

## Python Connection

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect(
        ws_endpoint='wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY'
    )
    page = browser.new_page()
    page.goto('https://example.com')
    browser.close()
```

## Java Connection

```java
import com.microsoft.playwright.*;

public class Main {
    public static void main(String[] args) {
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connect(
                "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
            );
            Page page = browser.newPage();
            page.navigate("https://example.com");
            browser.close();
        }
    }
}
```

Maven dependency:

```xml
<dependency>
  <groupId>com.microsoft.playwright</groupId>
  <artifactId>playwright</artifactId>
  <version>1.58.0</version>
</dependency>
```

## C# Connection

```csharp
using Microsoft.Playwright;

using var playwright = await Playwright.CreateAsync();
var browser = await playwright.Chromium.ConnectAsync(
    "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
);
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");
await browser.CloseAsync();
```

Install the matching package:

```bash
dotnet add package Microsoft.Playwright --version 1.58.0
```

## Choose A Browser

Available browser names in the source example are `chromium`, `firefox`, and `webkit`.

### Node.js

```javascript
import { firefox } from 'playwright';

const browser = await firefox.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

### Python

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.firefox.connect(
        ws_endpoint='wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY'
    )
    page = browser.new_page()
    page.goto('https://example.com')
    browser.close()
```

### Java

```java
import com.microsoft.playwright.*;

public class Main {
    public static void main(String[] args) {
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.firefox().connect(
                "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
            );
            Page page = browser.newPage();
            page.navigate("https://example.com");
            browser.close();
        }
    }
}
```

### C#

```csharp
using Microsoft.Playwright;

using var playwright = await Playwright.CreateAsync();
var browser = await playwright.Firefox.ConnectAsync(
    "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
);
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");
await browser.CloseAsync();
```

## Screenshots And PDFs

### Node.js

```javascript
import { chromium } from 'playwright';
import fs from 'fs';

const browser = await chromium.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');

const pngBuffer = await page.screenshot();
fs.writeFileSync('screenshot.png', pngBuffer);

const pdfBuffer = await page.pdf({ format: 'A4' });
fs.writeFileSync('page.pdf', pdfBuffer);

await browser.close();
```

### Python

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect(
        ws_endpoint='wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY'
    )
    page = browser.new_page()
    page.goto('https://example.com')

    png_bytes = page.screenshot()
    with open('screenshot.png', 'wb') as f:
        f.write(png_bytes)

    pdf_bytes = page.pdf(format='A4')
    with open('page.pdf', 'wb') as f:
        f.write(pdf_bytes)

    browser.close()
```

### Java

```java
import com.microsoft.playwright.*;
import java.nio.file.Paths;

try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connect(
        "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
    );
    Page page = browser.newPage();
    page.navigate("https://example.com");

    page.screenshot(new Page.ScreenshotOptions()
        .setPath(Paths.get("screenshot.png")));

    page.pdf(new Page.PdfOptions()
        .setPath(Paths.get("page.pdf")));

    browser.close();
}
```

### C#

```csharp
using Microsoft.Playwright;

using var playwright = await Playwright.CreateAsync();
var browser = await playwright.Chromium.ConnectAsync(
    "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
);
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");

await page.ScreenshotAsync(new PageScreenshotOptions { Path = "screenshot.png" });
await page.PdfAsync(new PagePdfOptions { Path = "page.pdf" });

await browser.CloseAsync();
```

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
