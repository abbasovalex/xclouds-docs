# Обзор xClouds

xClouds дает разработчикам удаленные браузеры для автоматизации и dev tunnel для локальной разработки.

Используйте xClouds, когда нужно:

- запускать Selenium через удаленный WebDriver endpoint;
- подключать Playwright к удаленному браузеру по WebSocket;
- подключать Puppeteer, CDP-инструменты или AI browser agents к Chrome DevTools Protocol endpoint;
- открыть локальное приложение через публичный HTTPS URL для webhooks, callbacks, демо и браузерных тестов.

## Endpoints

| Сценарий | Endpoint |
| --- | --- |
| Selenium | `http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY` |
| Playwright | `wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY` |
| Puppeteer / CDP | `wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY` |
| Dev tunnel | `xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080` |

## С чего начать

Выберите страницу под свою задачу:

- [Dev tunnel](/ru/examples/dev_tunnel): открыть `localhost:8080` через публичный HTTPS URL.
- [Selenium](/ru/examples/selenium): подключить Python Selenium к xClouds.
- [Playwright](/ru/examples/playwright): подключить Playwright на Node.js, Python, Java или C#.
- [Puppeteer и CDP](/ru/examples/puppeteer_cdp): подключить Puppeteer, Playwright CDP или browser-use.

## Храните ключи приватно

В примерах используются `YOUR_API_KEY` и `YOUR_TUNNEL_TOKEN`. Замените их на значения из аккаунта xClouds и не коммитьте реальные ключи в Git.
