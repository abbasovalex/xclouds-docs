# Подключение к Selenium

Используйте этот пример, если у вас уже есть Selenium-тесты и вы хотите запускать их через xClouds.
<!-- tabs:start -->
#### **Python**

```bash
pip install selenium urllib3
```
[connect_to_xclouds.py](../../code_examples/selenium/python/connect_to_xclouds.py ':include :type=code python')

<!-- tabs:end -->

Ожидаемый результат:

```text
Скрипт печатает HTML страницы, полученный из удаленного браузера.
```

## Выбор настроек браузера

Пример из приложения задает версию браузера, стратегию загрузки страницы и платформу.

<!-- tabs:start -->
#### **Python**

[choose_browser.py](../../code_examples/selenium/python/choose_browser.py ':include :type=code python')
<!-- tabs:end -->


## Chrome Options

<!-- tabs:start -->
#### **Python**

[chrome_options.py](../../code_examples/selenium/python/chrome_options.py ':include :type=code python')
<!-- tabs:end -->

## Частые ошибки

| Симптом | Возможная причина | Как исправить |
| --- | --- | --- |
| `Host is unavailable` | Endpoint недоступен | Проверьте сеть и URL endpoint |
| Ошибка авторизации | API key отсутствует или неверный | Замените `YOUR_API_KEY` на Selenium key из xClouds |
| Сессия стартует, но страница не открывается | Сайт блокирует запрос или долго отвечает | Проверьте простой URL, например `https://example.com` |
| Настройки браузера не применяются | Capability не поддерживается | Начните с базового примера и добавляйте options по одному |
| Тест зависает | `driver.quit()` не был вызван | В production-тестах используйте `try/finally` |

## Предостережения

<p class="tip">
    Не храните API ключ в исходном коде, используйте для этого переменные окружения или специальные менеджеры для хранения чувствительной информации. Закрывайте браузер после каждого запуска, особенно в CI и регулярных задачах,
    чтобы избежать выгорания ваших минут и кредитов.
</p>