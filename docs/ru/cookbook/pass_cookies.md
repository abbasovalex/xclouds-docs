# Передача cookies в браузеры

Зачастую требуется передавать cookies для сложных сценариев тестирования.
Также передача cookies требуется при большинстве задач парсинга/скрапинга открытых данных.
В Selenium, Playwright и Puppeteer/CDP для этого есть специальные методы.
Мы подготовили простые примеры с использованием в качестве подопытного `httpbin.org`.
Эти примеры помогут вам подключить и использовать cookies в своих тестах и скриптах по сбору данных.

## Selenium

В этом примере мы продемонстрируем как передавать cookies при работе с Selenium.
При работе с cookies в Selenium есть важная особенность — cookies добавляются только после того, как вы запросили нужный вам URI.
Проще говоря, вы сначала открываете нужный URI, а затем добавляете к нему cookies.
После этого нужно сделать рефреш текущей страницы или запросить целевую страницу.

<!-- tabs:start -->
#### **python**
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
    driver.get("https://httpbin.xclouds.dev")

    driver.add_cookie({
        "name": "session_id",
        "value": "demo-cookie-value",
        "path": "/",
    })
    driver.refresh()
    
    driver.get("https://httpbin.xclouds.dev/cookies")
    print(driver.execute_script("return document.body.innerText"))
finally:
    driver.quit()
```

<!-- tabs:end -->

Ожидаемый результат:

```text
{
  "cookies": {
    "session_id": "demo-cookie-value"
  }
}
```

На практике обычно требуется передавать сразу весь набор cookies.
Используйте следующий пример для чтения всех cookies из файла и передачи его браузеру:

<!-- tabs:start -->
#### **python**

```python
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

def load_cookies_from_file(driver, cookie_path):
    if not cookie_path.exists():
        raise FileNotFoundError(f"Cookie file not found: {cookie_path}")

    cookies = json.loads(cookie_path.read_text(encoding="utf-8"))
    if not isinstance(cookies, list):
        raise ValueError("Cookie file must be an EditThisCookie-style JSON list.")

    for cookie in cookies:
        item = {
            "name": cookie["name"],
            "value": cookie["value"],
            "path": cookie.get("path", "/"),
            "domain": cookie.get("domain"),
            "secure": bool(cookie.get("secure", True)),
        }
        expiration = cookie.get("expirationDate") or cookie.get("expiry")
        if expiration:
            item["expiry"] = int(expiration)
        driver.add_cookie(item)


driver = webdriver.Remote(
    command_executor=XCLOUDS_URL,
    options=ChromeOptions(),
)

try:
    driver.get("https://httpbin.xclouds.dev")
    load_cookies_from_file(driver, '~/my_cookies.json')
    driver.refresh()

    driver.get("https://httpbin.xclouds.dev/cookies")
    print(driver.execute_script("return document.body.innerText"))
finally:
    driver.quit()
```
<!-- tabs:end -->

Есть несколько способов достать cookies из браузера. Но самый простой через дополнение в Chrome.
1. Установите дополнение <a href="https://chromewebstore.google.com/detail/editthiscookie-v3/ojfebgpkimhlhcblbalbfjblapadhbol">EditThisCookie (V3)</a> для Chrome
2. Посетите нужную страницу
3. Откройте EditThisCookie и сделайте export (данные копируются в буфер)
4. Создайте в домашней директории файл `my_cookies.json` и вставьте в него то, что у вас в буфере (технически в буфере находится список в формате JSON). 

<p class="warn">
    Больше деталей в <a href="https://www.selenium.dev/documentation/webdriver/interactions/cookies/">официальной документации по Selenium</a>
</p>


## Playwright

В Playwright cookies удобнее добавить в browser context до создания страницы.
<!-- tabs:start -->
#### **JavaScript**

Сейчас на серверах xclouds используется версия playwright == 1.58. Очень важно чтобы на клиенте стояла библиотека версии 1.58.
Если вы установите более свежую или старую версию, то возникнут проблемы при запуске тестов. 
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
  domain: 'httpbin.xclouds.dev',
  path: '/',
}]);

const page = await context.newPage();
await page.goto('https://httpbin.xclouds.dev/cookies');

console.log(await page.textContent('body'));

await browser.close();
```
<!-- tabs:end -->
Ожидаемый результат:

```text
{
  "cookies": {
    "session_id": "demo-cookie-value"
  }
}
```
<p class="warn">
    Больше деталей в <a href="https://playwright.dev/docs/api/class-browsercontext#browser-context-add-cookies">официальной документации по Playwright</a>
</p>

## Puppeteer

В Puppeteer подключитесь к CDP endpoint xClouds и добавьте cookie через browser context.

<!-- tabs:start -->
#### **JavaScript**
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
  domain: 'httpbin.xclouds.dev',
  path: '/',
});

const page = await context.newPage();
await page.goto('https://httpbin.xclouds.dev/cookies');

console.log(await page.$eval('body', element => element.innerText));

await browser.close();
```
<!-- tabs:end -->

Ожидаемый результат:

```text
{
  "cookies": {
    "session_id": "demo-cookie-value"
  }
}
```
<p class="warn">
    Больше деталей в <a href="https://pptr.dev/api/puppeteer.browsercontext.setcookie">официальной документации по Puppeteer</a>
</p>

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| Cookie не появилась | Домен cookie не совпадает с доменом страницы | Используйте тот же домен, например `httpbin.org` для `https://httpbin.org/cookies` |
| Selenium выдает ошибку при `add_cookie()` | Браузер еще не открыт на нужном домене | Сначала вызовите `driver.get("https://httpbin.xclouds.dev")` |
| Сайт все равно просит логин | Передана не вся сессия | Проверьте, какие cookies реально нужны приложению |
| Cookie видна в коде, но не в `document.cookie` | У cookie стоит флаг `HttpOnly` | Это нормально: браузер отправляет такую cookie на сервер, но JavaScript ее не читает |
| Пример не подключается к xClouds | Неверный endpoint или API key | Проверьте URL и замените `YOUR_API_KEY` на свой ключ |

## Предостережения

<p class="tip">
    Не храните реальные cookies в репозитории. Передавайте ссылку на файл через переменные окружения,
    который не попадет в Git. После теста обязательно закрывайте браузер через `driver.quit()` или `browser.close()`,
    чтобы избежать выгорания ваших минут и кредитов.
</p>
