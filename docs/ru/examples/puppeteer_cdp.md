# Пример Puppeteer и CDP

Используйте этот пример, когда нужен Chrome DevTools Protocol endpoint для Puppeteer, Playwright CDP workflow или AI browser automation frameworks.

## Что нужно

```bash
npm install puppeteer
```

## Подключение Puppeteer

```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.connect({
    browserWSEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY'
});

const page = await browser.newPage();

await page.goto('https://example.com');
const title = await page.title();
console.log(`Page title: "${title}"`);

await browser.close();
```

Ожидаемый вывод:

```text
Page title: "Example Domain"
```

## Playwright через CDP

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connect({
    wsEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY',
});

const page = await browser.newPage();
const client = await page.context().newCDPSession(page);
await client.send('Animation.enable');
client.on('Animation.animationCreated', () => console.log('Animation created!'));
const response = await client.send('Animation.getPlaybackRate');
console.log('playback rate is ' + response.playbackRate);
await client.send('Animation.setPlaybackRate', {
  playbackRate: response.playbackRate / 2
});
```

## browser-use Agent

```python
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

BROWSER_USE_API_KEY = 'your browser-use api key'

async def main():
    browser = Browser(cdp_url='wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY')
    agent = Agent(
        task='Visit https://habr.com/ and search for "vpn"',
        browser=browser,
        llm=ChatBrowserUse(api_key=BROWSER_USE_API_KEY),
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
```

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| Puppeteer не подключается | Неверный CDP endpoint | Используйте `wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY` |
| Ошибка авторизации | API key отсутствует или неверный | Замените `YOUR_API_KEY` на CDP key из xClouds |
| CDP command падает | Команда не поддерживается в текущем контексте браузера | Сначала проверьте простой `page.goto()` |
| Agent не запускается | Не указан внешний LLM key | Передайте key, который требует ваш agent framework |
| Сессия остается открытой | Браузер не закрыли | В конце задачи вызовите `await browser.close()` |

## Для production

CDP дает мощный контроль над браузером. Храните API keys приватно, изолируйте недоверенные automation tasks и закрывайте сессии после завершения работы.
