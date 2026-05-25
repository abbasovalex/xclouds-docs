# Пример Puppeteer и CDP

Используйте этот пример, когда нужен Chrome DevTools Protocol endpoint для Puppeteer, Playwright CDP workflow или AI browser automation frameworks.

## Подключение к Puppeteer
<!-- tabs:start -->
#### **JavaScript**

```bash
npm install puppeteer
```

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
<!-- tabs:end -->

Ожидаемый вывод:

```text
Page title: "Example Domain"
```

## Подключение к Playwright через CDP
<!-- tabs:start -->
#### **JavaScript**

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
<!-- tabs:end -->


## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| Puppeteer не подключается | Неверный CDP endpoint | Используйте `wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY` |
| Ошибка авторизации | API key отсутствует или неверный | Замените `YOUR_API_KEY` на CDP key из xClouds |
| CDP command падает | Команда не поддерживается в текущем контексте браузера | Сначала проверьте простой `page.goto()` |
| Agent не запускается | Не указан внешний LLM key | Передайте key, который требует ваш agent framework |
| Сессия остается открытой | Браузер не закрыли | В конце задачи вызовите `await browser.close()` |


## Предостережения

<p class="tip">
    Не храните API ключ в исходном коде, используйте для этого переменные окружения или специальные менеджеры для хранения чувствительной информации. Закрывайте браузер после каждого запуска, особенно в CI и регулярных задачах, 
    чтобы избежать выгорания ваших минут и кредитов.
</p>
