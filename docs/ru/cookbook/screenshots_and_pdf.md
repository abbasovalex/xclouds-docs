# Скриншоты и PDF

## Создание скриншотов и PDF в Playwright

<!-- tabs:start -->

#### **JavaScript**

[playwright_screenshots_pdf.js](../../code_examples/cookbook/screenshots_and_pdf/javascript/playwright_screenshots_pdf.js ':include :type=code javascript')

#### **Python**

[playwright_screenshots_pdf.py](../../code_examples/cookbook/screenshots_and_pdf/python/playwright_screenshots_pdf.py ':include :type=code python')

#### **Java**

[playwright_screenshots_pdf.java](../../code_examples/cookbook/screenshots_and_pdf/java/playwright_screenshots_pdf.java ':include :type=code java')

#### **C#**

[playwright_screenshots_pdf.cs](../../code_examples/cookbook/screenshots_and_pdf/csharp/playwright_screenshots_pdf.cs ':include :type=code csharp')
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