# Работа с прокси провайдерами

xClouds может запускать удаленный браузер через ваш сторонний `http` или `https` прокси.
Это полезно, когда ваш сценарий зависит от географии, IP-репутации или уже купленного прокси-провайдера, а код автоматизации вы хотите оставить в привычном Puppeteer или Playwright CDP.

Эта страница помогает проверить простое решение: передать прокси в CDP endpoint xClouds, открыть `https://ipinfo.io/ip` и убедиться, что сайт видит IP прокси, а не обычный IP браузерного пула.
После этого можно перейти к более практичному примеру с cookies, заголовками и `TARGET_URL` для сайтов со строгими проверками, например Wildberries.

## Что понадобится

- CDP API key из личного кабинета xClouds.
- URL стороннего прокси в формате `http://user:password@proxy.example.com:8080` или `https://user:password@proxy.example.com:8443`.
- Node.js и один из клиентов:

<!-- tabs:start -->
#### **Puppeteer**

```bash
npm install puppeteer
```

#### **Playwright CDP**

```bash
npm install playwright@1.58
```
<!-- tabs:end -->

<p class="tip">
    Прокси передается в CDP endpoint через параметр <code>externalProxyServer</code>.
    Значение прокси нужно кодировать через <code>encodeURIComponent</code>, потому что в URL обычно есть логин, пароль, двоеточия и символ <code>@</code>.
</p>

## Проверка IP через ipinfo.io

Начните с короткого smoke-теста.
Он открывает `https://ipinfo.io/ip` и печатает IP, который увидел внешний сайт.
Если прокси настроен правильно, в выводе будет IP вашего прокси-провайдера.

<!-- tabs:start -->
#### **Puppeteer**

```javascript
import puppeteer from 'puppeteer';

const apiKey = process.env.XCLOUDS_CDP_API_KEY;
const proxyServer = process.env.EXTERNAL_PROXY_SERVER;

if (!apiKey || !proxyServer) {
  throw new Error('Set XCLOUDS_CDP_API_KEY and EXTERNAL_PROXY_SERVER');
}

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', apiKey);
endpoint.searchParams.set('externalProxyServer', proxyServer);

const browser = await puppeteer.connect({
  browserWSEndpoint: endpoint.toString(),
});

try {
  const page = await browser.newPage();
  await page.goto('https://ipinfo.io/ip', { waitUntil: 'networkidle2', timeout: 45000 });

  const ip = (await page.$eval('body', element => element.innerText)).trim();
  if (!ip) {
    throw new Error('ipinfo.io returned an empty response');
  }

  console.log(`Proxy IP: ${ip}`);
} finally {
  await browser.close();
}
```

#### **Playwright CDP**

```javascript
import { chromium } from 'playwright';

const apiKey = process.env.XCLOUDS_CDP_API_KEY;
const proxyServer = process.env.EXTERNAL_PROXY_SERVER;

if (!apiKey || !proxyServer) {
  throw new Error('Set XCLOUDS_CDP_API_KEY and EXTERNAL_PROXY_SERVER');
}

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', apiKey);
endpoint.searchParams.set('externalProxyServer', proxyServer);

const browser = await chromium.connectOverCDP(endpoint.toString());

try {
  const context = browser.contexts()[0] || await browser.newContext();
  const page = await context.newPage();
  await page.goto('https://ipinfo.io/ip', { waitUntil: 'networkidle', timeout: 45000 });

  const ip = (await page.textContent('body'))?.trim();
  if (!ip) {
    throw new Error('ipinfo.io returned an empty response');
  }

  console.log(`Proxy IP: ${ip}`);
} finally {
  await browser.close();
}
```
<!-- tabs:end -->

Запуск:

```bash
XCLOUDS_CDP_API_KEY=YOUR_API_KEY \
EXTERNAL_PROXY_SERVER='http://user:password@proxy.example.com:8080' \
node docs/scripts/python/third_party_proxy_puppeteer_cdp.js
```

Готовые файлы примеров:

- [third_party_proxy_puppeteer_cdp.js](/scripts/python/third_party_proxy_puppeteer_cdp.js)
- [third_party_proxy_playwright_cdp.js](/scripts/python/third_party_proxy_playwright_cdp.js)

Ожидаемый результат:

```text
Proxy IP: 203.0.113.10
```

## Пример для сайта со строгими проверками

Для реальных задач парсинга часто мало просто сменить IP.
Сайт может учитывать cookies, язык, user-agent, заголовки и обычное поведение браузера.
В примере ниже целевой URL задается через `TARGET_URL`.
По умолчанию используется `https://www.wildberries.ru/`, но для своих тестов лучше явно передать нужную страницу.

`COOKIE_JSON` — необязательная переменная.
Она принимает JSON-массив cookies в формате, близком к Playwright/Puppeteer:

```json
[
  {
    "name": "session_id",
    "value": "demo-cookie-value",
    "domain": ".example.com",
    "path": "/",
    "secure": true,
    "httpOnly": true
  }
]
```

<!-- tabs:start -->
#### **Puppeteer**

```javascript
import puppeteer from 'puppeteer';

const apiKey = process.env.XCLOUDS_CDP_API_KEY;
const proxyServer = process.env.EXTERNAL_PROXY_SERVER;
const targetUrl = process.env.TARGET_URL || 'https://www.wildberries.ru/';
const userAgent = process.env.USER_AGENT || [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'AppleWebKit/537.36 (KHTML, like Gecko)',
  'Chrome/124.0.0.0 Safari/537.36',
].join(' ');
const cookies = process.env.COOKIE_JSON ? JSON.parse(process.env.COOKIE_JSON) : [];

if (!apiKey || !proxyServer) {
  throw new Error('Set XCLOUDS_CDP_API_KEY and EXTERNAL_PROXY_SERVER');
}

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', apiKey);
endpoint.searchParams.set('externalProxyServer', proxyServer);

const browser = await puppeteer.connect({
  browserWSEndpoint: endpoint.toString(),
});

try {
  const page = await browser.newPage();
  await page.setUserAgent(userAgent);
  await page.setExtraHTTPHeaders({
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
  });

  if (cookies.length > 0) {
    await page.setCookie(...cookies);
  }

  const response = await page.goto(targetUrl, {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });

  console.log(`Status: ${response?.status() ?? 'unknown'}`);
  console.log(`Title: ${await page.title()}`);
} finally {
  await browser.close();
}
```

#### **Playwright CDP**

```javascript
import { chromium } from 'playwright';

const apiKey = process.env.XCLOUDS_CDP_API_KEY;
const proxyServer = process.env.EXTERNAL_PROXY_SERVER;
const targetUrl = process.env.TARGET_URL || 'https://www.wildberries.ru/';
const userAgent = process.env.USER_AGENT || [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'AppleWebKit/537.36 (KHTML, like Gecko)',
  'Chrome/124.0.0.0 Safari/537.36',
].join(' ');
const cookies = process.env.COOKIE_JSON ? JSON.parse(process.env.COOKIE_JSON) : [];

if (!apiKey || !proxyServer) {
  throw new Error('Set XCLOUDS_CDP_API_KEY and EXTERNAL_PROXY_SERVER');
}

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', apiKey);
endpoint.searchParams.set('externalProxyServer', proxyServer);

const browser = await chromium.connectOverCDP(endpoint.toString());

try {
  const context = browser.contexts()[0] || await browser.newContext();
  await context.setExtraHTTPHeaders({
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
  });

  if (cookies.length > 0) {
    await context.addCookies(cookies);
  }

  const page = await context.newPage();
  await page.setExtraHTTPHeaders({ 'User-Agent': userAgent });

  const response = await page.goto(targetUrl, {
    waitUntil: 'domcontentloaded',
    timeout: 60000,
  });

  console.log(`Status: ${response?.status() ?? 'unknown'}`);
  console.log(`Title: ${await page.title()}`);
} finally {
  await browser.close();
}
```
<!-- tabs:end -->

Запуск расширенного примера:

```bash
XCLOUDS_CDP_API_KEY=YOUR_API_KEY \
EXTERNAL_PROXY_SERVER='http://user:password@proxy.example.com:8080' \
TARGET_URL='https://www.wildberries.ru/' \
COOKIE_JSON='[{"name":"session_id","value":"demo","domain":".wildberries.ru","path":"/"}]' \
node docs/scripts/python/third_party_proxy_playwright_cdp.js
```

## Правила для externalProxyServer

| Правило | Что это значит |
| --- | --- |
| Поддерживаются только `http` и `https` | `socks5://...` не подойдет для этого endpoint |
| Нужен явный порт | Используйте `proxy.example.com:8080`, а не просто `proxy.example.com` |
| Хост должен быть публичным | `localhost`, `127.0.0.1`, `10.0.0.5` и другие приватные адреса будут отклонены |
| Не смешивайте с `proxy=residential` | Выберите либо встроенный режим, либо свой `externalProxyServer` |
| Логин и пароль можно передавать в URL | Например `http://user:password@proxy.example.com:8080` |

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| `externalProxyServer scheme must be http or https` | Передан SOCKS или другой неподдерживаемый протокол | Используйте `http://` или `https://` прокси |
| `externalProxyServer must include an explicit port` | В URL прокси нет порта | Добавьте порт, например `:8080` или `:8443` |
| `externalProxyServer host is not public` | Передан локальный или приватный адрес | Используйте публичный адрес прокси-провайдера |
| Подключение к CDP не проходит | Неверный xClouds API key или прокси недоступен | Сначала проверьте ключ, затем проверьте прокси у провайдера |
| `ipinfo.io` показывает не тот IP | Прокси не применился или провайдер выдал другой выходной IP | Проверьте значение `EXTERNAL_PROXY_SERVER` и настройки кабинета прокси |
| Сайт возвращает 403 или капчу | Одного прокси недостаточно для этого сайта | Проверьте cookies, заголовки, частоту запросов и правила сайта |
| Cookies не работают | Домен cookie не совпадает с `TARGET_URL` | Укажите домен целевого сайта, например `.example.com` |

## Предостережения

<p class="tip">
    Не храните CDP API key, URL прокси и реальные cookies в коде или Git.
    Передавайте их через переменные окружения, секреты CI или менеджер секретов.
</p>

Для продакшена учитывайте лимиты прокси-провайдера, правила целевого сайта, robots.txt и юридические ограничения на сбор данных.
Прокси помогает выбрать маршрут трафика, но не отменяет требования к разрешенному доступу, бережной частоте запросов и корректной работе с персональными данными.
Всегда закрывайте браузер через `browser.close()`, чтобы сессия xClouds завершалась после выполнения задачи.

## Источники

- <a href="https://pptr.dev/api/puppeteer.puppeteer.connect" target="_blank">Puppeteer: подключение к существующему браузеру</a>
- <a href="https://pptr.dev/api/puppeteer.page.setextrahttpheaders" target="_blank">Puppeteer: дополнительные HTTP-заголовки</a>
- <a href="https://playwright.dev/docs/api/class-browsertype#browser-type-connect-over-cdp" target="_blank">Playwright: подключение через CDP</a>
- <a href="https://playwright.dev/docs/api/class-browsercontext#browser-context-add-cookies" target="_blank">Playwright: cookies в browser context</a>
- <a href="https://chromedevtools.github.io/devtools-protocol/tot/Network/#method-setExtraHTTPHeaders" target="_blank">Chrome DevTools Protocol: Network.setExtraHTTPHeaders</a>
