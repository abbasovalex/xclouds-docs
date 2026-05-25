# Пример Playwright

Используйте этот пример, когда нужно подключить Playwright к браузеру, который запущен в xClouds.
<p class="tip">
    Версия playwright-клиента должна совпадать с версией endpoint. В пример мы используем версию 1.58
    Доступные версии можно увидеть в <a href="https://xclouds.dev/playwright/overview/" target="_blank">личном кабинете</a>.
</p>

<!-- tabs:start -->
#### **JavaScript**
```bash
npm install playwright@1.58
```

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

#### **Python**
```bash
pip install playwright==1.58
```

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

#### **Java**

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

#### **C#**

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
<!-- tabs:end -->

## Выбор браузера
В примерах ниже используется браузер Firefox. Кроме него вам также доступны Chromium и webkit.

<!-- tabs:start -->
#### **JavaScript**

```javascript
import { firefox } from 'playwright';

const browser = await firefox.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
```

#### **Python**

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

#### **Java**

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

#### **C#**

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
<!-- tabs:end -->


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
