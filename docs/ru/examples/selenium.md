# Подключение к Selenium

Используйте этот пример, если у вас уже есть Selenium-тесты и вы хотите запускать их через xClouds.
<!-- tabs:start -->
#### **Python**

```bash
pip install selenium urllib3
```

```python
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib3.exceptions import MaxRetryError

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

try:
    driver = webdriver.Remote(command_executor=XCLOUDS_URL, options=ChromeOptions())
    driver.get("https://google.com")
    print(driver.page_source)
    driver.quit()
except WebDriverException as e:
    print(f"Error: {e.msg}")
except MaxRetryError:
    print("Host is unavailable")
```
<!-- tabs:end -->

Ожидаемый результат:

```text
Скрипт печатает HTML страницы, полученный из удаленного браузера.
```

## Выбор настроек браузера

Пример из приложения задает версию браузера, стратегию загрузки страницы и платформу.

<!-- tabs:start -->
#### **Python**
```python
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib3.exceptions import MaxRetryError

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

options = ChromeOptions()
options.browser_version = "111.0"
options.page_load_strategy = "normal"
options.platform_name = "linux"

try:
    driver = webdriver.Remote(command_executor=XCLOUDS_URL, options=options)
    driver.get("https://google.com")
    print(driver.page_source)
    driver.quit()
except WebDriverException as e:
    print(f"Error: {e.msg}")
except MaxRetryError:
    print("Host is unavailable")
```
<!-- tabs:end -->


## Chrome Options

<!-- tabs:start -->
#### **Python**

```python
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from urllib3.exceptions import MaxRetryError

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

options = ChromeOptions()
options.browser_version = "111.0"
options.page_load_strategy = "normal"
options.platform_name = "linux"

options.add_argument("--start-maximized")
options.add_argument("--no-first-run")
options.add_experimental_option(
    "excludeSwitches",
    ["load-extension", "enable-automation", "enable-logging"],
)

try:
    driver = webdriver.Remote(command_executor=XCLOUDS_URL, options=options)
    driver.get("https://google.com")
    print(driver.page_source)
    driver.quit()
except WebDriverException as e:
    print(f"Error: {e.msg}")
except MaxRetryError:
    print("Host is unavailable")
```
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