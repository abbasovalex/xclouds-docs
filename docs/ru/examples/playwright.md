# Пример Playwright

Используйте этот пример, когда нужно подключить Playwright к браузеру, который запущен в xClouds.

## Что нужно

Версия Playwright-клиента должна совпадать с версией endpoint.

```bash
npm install playwright@1.58
```

Для Python:

```bash
pip install playwright==1.58
```

## Подключение на Node.js

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

## Подключение на Python

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

## Подключение на Java

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

## Подключение на C#

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

Установите подходящую версию пакета:

```bash
dotnet add package Microsoft.Playwright --version 1.58.0
```

## Выбор браузера

В исходном примере доступны `chromium`, `firefox` и `webkit`.

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

## Скриншоты и PDF

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

Ожидаемый результат:

```text
В текущей директории появятся screenshot.png и page.pdf.
```

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| Подключение отклонено | API key отсутствует или неверный | Замените `YOUR_API_KEY` на Playwright key из xClouds |
| Protocol error после подключения | Версии клиента и endpoint не совпадают | Используйте `playwright@1.58` вместе с `/v1.58/` |
| PDF не создается | PDF работает только в Chromium | Используйте `chromium.connect(...)` |
| Выбор браузера не работает | Import не совпадает с выбранным браузером | Явно импортируйте `chromium`, `firefox` или `webkit` |
| Скрипт завершается раньше времени | Не хватает `await` | Дождитесь навигации и записи файлов перед закрытием |

## Для production

Храните API keys вне исходного кода. Закрывайте браузер после каждого запуска, особенно в CI и регулярных задачах.
