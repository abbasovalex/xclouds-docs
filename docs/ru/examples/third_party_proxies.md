# Запуск браузеров через proxy

Работа браузеров с прокси широко используются как для сценариев тестирования, так и для сбора данных через интернет (скрапинг, парсинг).
Для тестирования прокси может использоваться в сценариях e2e-тестов, когда ваш сервер закрыт от внешнего мира и к нему есть доступ только с прокси-сервера.
Другой пример — собрать для службы маркетинга данные по конкуренту, но не просто собрать, а с учетом конкретного региона (страны, города).

xClouds поддерживает работу с proxy. Это означает, что вы можете запускать наши браузеры и 
они будут обращаться к нужным URI через ваш или сторонний proxy-сервер. Далее мы покажем 
как использовать прокси на примере Playwright, Puppeteer и CDP.

## Что понадобится

- [API ключ для CDP](https://xclouds.dev/ru/puppeteer/get-started/) из личного кабинета на xClouds
- Данные прокси-сервера в формате `http://user:password@proxy.server.com:8080` или `https://user:password@proxy.server.com:8443`.
Внимание: proxy.server.com — это вымышленный сервер для примеров, используйте вместо него настоящий прокси-сервер.
- Установленные на вашем ПК Puppeteer или Playwright:

<!-- tabs:start -->
#### **Puppeteer**

```bash
npm install puppeteer
```

#### **Playwright**

```bash
npm install playwright@1.58
```
<!-- tabs:end -->

## Базовый пример

Начнём с простого теста. Всё что он делает — посещает сайт `https://httpbin.xclouds.dev/ip` и печатает наш IP.
Если мы посетим этот сайт через прокси, то он отобразит IP адрес прокси-сервера.

<!-- tabs:start -->
#### **Puppeteer**

```javascript
// proxy_via_cdp.js
import puppeteer from 'puppeteer';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'https://user:password@proxy.server.com:8433');

const browser = await puppeteer.connect({
  browserWSEndpoint: endpoint.toString(),
});

try {
  const page = await browser.newPage();
  const response = await page.goto('https://httpbin.xclouds.dev/ip');
  const data = await response.json();
  console.log(`Proxy IP: ${data.origin}`);
} finally {
  await browser.close();
}
```

#### **Playwright**

```javascript
// proxy_via_cdp.js
import { chromium } from 'playwright';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'http://user:password@proxy.server.com:8080');

const browser = await chromium.connectOverCDP(endpoint.toString());

try {
  const context = browser.contexts()[0] || await browser.newContext();
  const page = await context.newPage();
  const response = await page.goto('https://httpbin.xclouds.dev/ip');
  const data = await response.json();
  console.log(`Proxy IP: ${data.origin}`);
} finally {
  await browser.close();
}
```
<!-- tabs:end -->

Запускаем этот скрипт через консоль:

```bash
node ./proxy_via_cdp.js
```


## Расширенный пример с передачей заголовков и cookies

Базовый пример демонстрирует суть работы прокси — ваши запросы идут с других IP.
В реальных задачах требуется не только наличие прокси, но 
также передача дополнительных данных через заголовки (headers) и cookies.
Давайте продемонстрируем на примере ниже как их передавать вместе с прокси. 

<p class="tip">
Для упрощения примеров мы вставляем прямо в код скрипта api ключи, пароли и cookies. 
На практике не делайте так. Правильно будет передавать эти данные через переменные окружения.
</p>

<!-- tabs:start -->
#### **Puppeteer**

```javascript
// proxy_via_cdp_with_custom_headers_and_cookie.js
import puppeteer from 'puppeteer';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'http://user:password@proxy.server.com:8080');

const browser = await puppeteer.connect({
  browserWSEndpoint: endpoint.toString(),
});

try {

  // Добавляем cookies в браузер
  const cookies = JSON.parse('[{"name":"session_id","value":"demo","domain":".xclouds.dev","path":"/"}]');
  await browser.setCookie(...cookies);

  const page = await browser.newPage();
  await page.setUserAgent({'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'});
  await page.setExtraHTTPHeaders({
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
  });

  // Выводит список cookies, которые получил от нашего приложения (при условии, что мы их верно передали)
  const response = await page.goto('https://httpbin.xclouds.dev/cookies');
  const data = await response.json();
  console.log(`Cookies: ${(JSON.stringify(data, null, 2))}`);

  // Выводит список заголовков которые наше приложение отправило
  const response2 = await page.goto('https://httpbin.xclouds.dev/headers');
  const data2 = await response2.json();
  console.log(`Headers: ${(JSON.stringify(data2, null, 2))}`);

} finally {
  await browser.close();
}
```

#### **Playwright**

```javascript
// proxy_via_cdp_with_custom_headers_and_cookie.js
import { chromium } from 'playwright';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'http://user:password@proxy.server.com:8080');

const browser = await chromium.connectOverCDP(endpoint.toString());
const context = browser.contexts()[0] || await browser.newContext();

try {

  await context.setExtraHTTPHeaders({
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
  });
  // Добавляем cookies в браузер
  const cookies = JSON.parse('[{"name":"session_id","value":"demo","domain":".xclouds.dev","path":"/"}]');
  await context.addCookies(cookies);

  const page = await context.newPage();
  await page.setExtraHTTPHeaders({'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'});


  // Отображает список cookies которые получил от нашего приложения (при условии, что мы их верно передали)
  const response = await page.goto('https://httpbin.xclouds.dev/cookies');
  const data = await response.json();
  console.log(`Cookies: ${(JSON.stringify(data, null, 2))}`);

  // Отображает список заголовков которые наше приложение отправило
  const response2 = await page.goto('https://httpbin.xclouds.dev/headers');
  const data2 = await response2.json();
  console.log(`Headers: ${(JSON.stringify(data2, null, 2))}`);

} finally {
  await browser.close();
}
```
<!-- tabs:end -->

Запуск расширенного примера:

```bash
node node ./proxy_via_cdp_with_custom_headers_and_cookie.js
```

## Частые ошибки

Проблемы при передаче данных через параметр **externalProxyServer**:

| Симптом                                                         | Что это значит                                                                                                                                                                                                                                                                                                                          |
|-----------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Неверный протокол                                               | Допускается только `http` и `https`. `socks5://...` и другие не подойдут.                                                                                                                                                                                                                                                               |
| Не указан порт                                                  | Используйте `proxy.server.com:8080`, а не просто `proxy.server.com`                                                                                                                                                                                                                                                                     |
| Пытаетесь использвоать прокси который недоступен через интернет | Хост вашего прокси-сервера должен быть публичным. Приватные адреса вида `localhost`, `127.0.0.1`, `10.0.0.5`,  `192.168.0.1`не подходят.                                                                                                                                                                                                |
| Прокси-сервер требует логин и пароль, но вы их не передаете     | Вы можете передавать логин и пароль в URL. Например `http://user:password@proxy.server.com:8080`                                                                                                                                                                                                                                        |
| Данные при передаче не закодированы                             | Значение прокси обязательно должно быть закодировано через `encodeURIComponent`, потому что в URL обычно есть логин, пароль, двоеточия и символ @. Если вы используете `searchParams.set`, то параметры кодируются автоматически. Но если вы используете другой подход, то убедитесь, чтобы параметры передавались в закодированном виде. |

Другие частые ошибки:

| Симптом                                    | Возможная причина                                                      | Как исправить                                                                                                                 |
|--------------------------------------------|------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| Подключение к CDP не проходит              | Неверный YOUR_API_KEY или прокси недоступен                            | Сначала проверьте ключ. Также убедитесь, что используете ключ для CDP. Если ключ верный, то проверьте прокси у провайдера     |
| `httpbin.xclouds.dev/ip` выводит не тот IP | Прокси не применился или провайдер выдал другой выходной IP            | Проверьте значение `PROXY_SERVER` и настройки кабинета прокси                                                                 |
| Сайт возвращает 403 или каптчу             | Одного прокси недостаточно для этого сайта                             | Проверьте cookies, заголовки, частоту запросов и правила сайта                                                                |
| Cookies не работают                        | Домен cookie не совпадает с доменом страницы которую вы хотите открыть | Укажите домен целевого сайта. Если обращаетесь к домену www.example.com, то в cookies должен быть указан домен `.example.com` |


## Предостережения

<p class="tip">
    Не храните CDP API key, URL прокси и реальные cookies в коде или Git.
    Передавайте их через переменные окружения, секреты CI или менеджер секретов.
</p>

Для продакшена учитывайте лимиты прокси-провайдера, правила целевого сайта, robots.txt и юридические ограничения на сбор данных.
Прокси помогает выбрать маршрут трафика, но не отменяет требования к разрешенному доступу, бережной частоте запросов и корректной работе с персональными данными.
Закрывайте браузер после каждого запуска, особенно в CI и регулярных задачах, чтобы избежать выгорания ваших минут и кредитов.
