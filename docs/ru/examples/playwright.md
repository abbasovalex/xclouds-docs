# Подключение к Playwright
Используйте этот пример, если у вас уже есть Playwright-тесты и вы хотите запускать их через xClouds.

<p class="tip">
    Версия playwright-клиента должна совпадать с версией endpoint. В пример мы используем версию 1.58
    Доступные версии можно увидеть в <a href="https://xclouds.dev/playwright/overview/" target="_blank">личном кабинете</a>.
</p>

<!-- tabs:start -->
#### **JavaScript**
```bash
npm install playwright@1.58
```

[chromium_connect.js](../../code_examples/playwright/javascript/chromium_connect.js ':include :type=code javascript')

#### **Python**
```bash
pip install playwright==1.58
```

[chromium_connect.py](../../code_examples/playwright/python/chromium_connect.py ':include :type=code python')

#### **Java**

[chromium_connect.java](../../code_examples/playwright/java/chromium_connect.java ':include :type=code java')

Maven dependency:

```xml
<dependency>
  <groupId>com.microsoft.playwright</groupId>
  <artifactId>playwright</artifactId>
  <version>1.58.0</version>
</dependency>
```

#### **C#**

[chromium_connect.cs](../../code_examples/playwright/csharp/chromium_connect.cs ':include :type=code csharp')

Установите подходящую версию пакета:

```bash
dotnet add package Microsoft.Playwright --version 1.58.0
```
<!-- tabs:end -->

## Выбор браузера
В примерах ниже используется браузер Firefox. Кроме него вам также доступны Chromium и webkit.

<!-- tabs:start -->
#### **JavaScript**

[firefox_connect.js](../../code_examples/playwright/javascript/firefox_connect.js ':include :type=code javascript')

#### **Python**

[firefox_connect.py](../../code_examples/playwright/python/firefox_connect.py ':include :type=code python')

#### **Java**

[firefox_connect.java](../../code_examples/playwright/java/firefox_connect.java ':include :type=code java')

#### **C#**

[firefox_connect.cs](../../code_examples/playwright/csharp/firefox_connect.cs ':include :type=code csharp')
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
