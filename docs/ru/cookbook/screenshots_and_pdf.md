# Скриншоты и PDF

## Создание скриншотов и PDF в Playwright

<!-- tabs:start -->

#### **JavaScript**

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

#### **Python**

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

#### **Java**

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

#### **C#**

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
<!-- tabs:end -->

Ожидаемый результат:

```text
В текущей директории появятся screenshot.png и page.pdf
```

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| Подключение отклонено | API key отсутствует или неверный | Замените `YOUR_API_KEY` на Playwright key из xClouds |
| Protocol error после подключения | Версии клиента и endpoint не совпадают | Используйте `playwright@1.58` вместе с `/v1.58/` |
| PDF не создается | PDF работает только в Chromium | Используйте `chromium.connect(...)` |
| Выбор браузера не работает | Import не совпадает с выбранным браузером | Явно импортируйте `chromium`, `firefox` или `webkit` |
| Скрипт завершается раньше времени | Не хватает `await` | Дождитесь навигации и записи файлов перед закрытием |

## Предостережения

<p class="tip">
    Не храните API ключ в исходном коде, используйте для этого переменные окружения или специальные менеджеры для хранения чувствительной информации. Закрывайте браузер после каждого запуска, особенно в CI и регулярных задачах, 
    чтобы избежать выгорания ваших минут и кредитов.
</p>