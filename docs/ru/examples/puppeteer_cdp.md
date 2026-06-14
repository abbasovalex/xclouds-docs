# Подключение через Puppeteer и CDP

Используйте эти примеры, если вы работаете с Puppeteer или предпочитаете подключаться к браузерам через CDP (Chrome DevTools Protocol) в своих скриптах.

## Подключение к Puppeteer
<!-- tabs:start -->
#### **JavaScript**

```bash
npm install puppeteer
```

[puppeteer_connect.js](../../code_examples/puppeteer_cdp/javascript/puppeteer_connect.js ':include :type=code javascript')
<!-- tabs:end -->

Ожидаемый вывод:

```text
Page title: "Example Domain"
```

## Подключение к CDP из Playwright
<!-- tabs:start -->
#### **JavaScript**

[playwright_cdp_connect.js](../../code_examples/puppeteer_cdp/javascript/playwright_cdp_connect.js ':include :type=code javascript')
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
