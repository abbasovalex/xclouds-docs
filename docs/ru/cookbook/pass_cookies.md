# Передача cookies в браузеры

Зачастую требуется передавать cookies для сложных сценариев тестирования.
Также передача cookies требуется при большинстве задач парсинга/скрапинга открытых данных.
В Selenium, Playwright и Puppeteer/CDP для этого есть специальные методы. Мы подготовили простые примеры, которые помогут вам подключить и использовать cookies в тестах и скриптах по сбору данных.

Ниже три коротких примера. Во всех примерах cookie добавляется для домена `httpbin.org`, а затем скрипт открывает `https://httpbin.org/cookies`. Этот сервис возвращает JSON с cookies, которые получил от браузера.

## Что нужно

- API key из xClouds для нужного endpoint.
- Cookie с правильным `name`, `value`, `domain` и `path`.
- Домен должен совпадать с сайтом, который вы открываете. Cookie для `httpbin.org` не будет работать на другом домене.

## Selenium

В Selenium сначала откройте страницу на нужном домене, а потом добавьте cookie.

```bash
pip install selenium
```

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

driver = webdriver.Remote(
    command_executor=XCLOUDS_URL,
    options=ChromeOptions(),
)

try:
    driver.get("https://httpbin.org")

    driver.add_cookie({
        "name": "session_id",
        "value": "demo-cookie-value",
        "path": "/",
    })

    driver.get("https://httpbin.org/cookies")
    print(driver.find_element("tag name", "body").text)
finally:
    driver.quit()
```

Ожидаемый результат:

```text
{
  "cookies": {
    "session_id": "demo-cookie-value"
  }
}
```

## Playwright

В Playwright cookies удобнее добавить в browser context до создания страницы.

```bash
npm install playwright@1.58
```

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connect({
  wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});

const context = await browser.newContext();

await context.addCookies([{
  name: 'session_id',
  value: 'demo-cookie-value',
  domain: 'httpbin.org',
  path: '/',
}]);

const page = await context.newPage();
await page.goto('https://httpbin.org/cookies');

console.log(await page.textContent('body'));

await browser.close();
```

Ожидаемый результат:

```text
{
  "cookies": {
    "session_id": "demo-cookie-value"
  }
}
```

## Puppeteer

В Puppeteer подключитесь к CDP endpoint xClouds и добавьте cookie через browser context.

```bash
npm install puppeteer
```

```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.connect({
  browserWSEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY',
});

const context = browser.defaultBrowserContext();

await context.setCookie({
  name: 'session_id',
  value: 'demo-cookie-value',
  domain: 'httpbin.org',
  path: '/',
});

const page = await context.newPage();
await page.goto('https://httpbin.org/cookies');

console.log(await page.$eval('body', element => element.innerText));

await browser.close();
```

Ожидаемый результат:

```text
{
  "cookies": {
    "session_id": "demo-cookie-value"
  }
}
```

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| Cookie не появилась | Домен cookie не совпадает с доменом страницы | Используйте тот же домен, например `httpbin.org` для `https://httpbin.org/cookies` |
| Selenium выдает ошибку при `add_cookie()` | Браузер еще не открыт на нужном домене | Сначала вызовите `driver.get("https://httpbin.org")` |
| Сайт все равно просит логин | Передана не вся сессия | Проверьте, какие cookies реально нужны приложению |
| Cookie видна в коде, но не в `document.cookie` | У cookie стоит флаг `HttpOnly` | Это нормально: браузер отправляет такую cookie на сервер, но JavaScript ее не читает |
| Пример не подключается к xClouds | Неверный endpoint или API key | Проверьте URL и замените `YOUR_API_KEY` на свой ключ |

## Для production

Не храните реальные cookies в репозитории. Передавайте их через переменные окружения, secret manager или временный файл, который не попадает в Git. После теста закрывайте браузер через `driver.quit()` или `browser.close()`, чтобы удаленная сессия завершилась.

## Источники

- httpbin — https://httpbin.org/
- Selenium WebDriver: Cookies — https://www.selenium.dev/documentation/webdriver/interactions/cookies/
- Playwright: BrowserContext `addCookies` — https://playwright.dev/docs/api/class-browsercontext#browser-context-add-cookies
- Puppeteer: BrowserContext `setCookie` — https://pptr.dev/api/puppeteer.browsercontext.setcookie
