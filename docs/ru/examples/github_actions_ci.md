# GitHub Actions CI с xClouds

xClouds может запускать браузерные сессии для CI через удаленные endpoints Playwright и Selenium. Используйте это руководство, если хотите, чтобы GitHub Actions выполнял браузерный smoke-тест без поддержки Selenium Grid, браузерных драйверов или браузерных узлов внутри runner.

## Контекст решения

- **Проблема:** браузерным тестам в CI нужны браузеры, драйверы и инфраструктура. Команды часто поддерживают Selenium Grid или устанавливают браузерные зависимости в каждый runner.
- **Решение:** используйте xClouds, когда GitHub Actions должен обращаться к удаленному браузерному endpoint вместо управления браузерными узлами в CI.
- **Когда подходит:** xClouds предоставляет Playwright WebSocket и Selenium WebDriver endpoints с аутентификацией по API-ключу.
- **Доказательство:** два smoke-скрипта подключаются к xClouds, открывают `https://example.com`, проверяют заголовок страницы и завершаются с ненулевым кодом, если удаленный браузер не сработал.

## Для кого эта страница

Эта страница для QA-инженеров, разработчиков и DevOps-инженеров, которые уже запускают тесты в GitHub Actions и хотят перенести выполнение браузеров в xClouds.

## Что вы соберете

Вы добавите один workflow GitHub Actions с двумя независимыми jobs:

- `playwright-smoke` подключается к `wss://playwright.xclouds.dev/v1.58/`.
- `selenium-smoke` подключается к `http://selenium.xclouds.dev/wd/hub`.

Обе jobs читают один и тот же secret `XCLOUDS_API_KEY` и запускают по одному самопроверяющемуся Python-скрипту.

## Требования

- Аккаунт xClouds и API-ключ.
- GitHub-репозиторий, где вы можете добавлять Actions secrets.
- Python-тесты или репозиторий, где допустим Python smoke-скрипт.

## 1. Добавьте GitHub Secret

В вашем GitHub-репозитории откройте **Settings -> Secrets and variables -> Actions -> New repository secret**.

Создайте secret с именем:

```text
XCLOUDS_API_KEY
```

В качестве значения используйте ваш API-ключ xClouds.

Workflow передает этот secret через блок `env`. Не помещайте API-ключ напрямую в файл workflow или в аргумент командной строки.

## 2. Добавьте smoke-скрипты

Скопируйте эти скрипты в ваш репозиторий:

- [github_actions_playwright_smoke.py](/scripts/python/github_actions_playwright_smoke.py)
- [github_actions_selenium_smoke.py](/scripts/python/github_actions_selenium_smoke.py)

В этом руководстве предполагается, что вы положите их сюда:

```text
scripts/xclouds/github_actions_playwright_smoke.py
scripts/xclouds/github_actions_selenium_smoke.py
```

Если вы используете другой путь, обновите команды workflow в следующем шаге.

## 3. Добавьте workflow GitHub Actions

Создайте `.github/workflows/xclouds-browser-tests.yml`:

[browser_tests.yml](../../code_examples/github_actions_ci/yaml/browser_tests.yml ':include :type=code yaml')

Jobs разделены, чтобы сбой Playwright и сбой Selenium было легко читать в интерфейсе Actions.

## 4. Проверьте запуск

Отправьте branch или откройте pull request. Workflow должен показать две успешно завершенные jobs.

Ожидаемый вывод Playwright:

```text
xClouds Playwright smoke test passed
```

Ожидаемый вывод Selenium:

```text
xClouds Selenium smoke test passed
```

Вы также можете запустить скрипты локально перед коммитом:

```bash
cd /path/to/your/repository
XCLOUDS_API_KEY=your_key python scripts/xclouds/github_actions_playwright_smoke.py
XCLOUDS_API_KEY=your_key python scripts/xclouds/github_actions_selenium_smoke.py
```

## Тестирование приватного UI в CI

Smoke-скрипты выше открывают публичную страницу. Если ваш репозиторий приватный и тестам нужно открыть ваш собственный UI, удаленному браузеру xClouds нужен публичный HTTPS URL для приложения, запущенного внутри GitHub Actions.

Для этого используйте dev tunnel xClouds:

1. Запустите приложение в GitHub Actions runner, например на порту `3000`.
2. Запустите `xclouds tunnel start --authtoken ... --port 3000`.
3. Передайте URL туннеля xClouds в тест как `BASE_URL`.
4. Настройте Playwright или Selenium так, чтобы они открывали `BASE_URL`, а не `localhost`.

Добавьте еще два secrets или variables:

| Имя | Тип | Назначение |
| --- | --- | --- |
| `XCLOUDS_TUNNEL_TOKEN` | Secret | Токен, который xClouds CLI использует для запуска dev tunnel |
| `XCLOUDS_TUNNEL_URL` | Repository variable или secret | Ваш назначенный URL туннеля, например `https://your-subdomain.tunnel.xclouds.dev` |

Пример формы job:

[private_ui_tests.yml](../../code_examples/github_actions_ci/yaml/private_ui_tests.yml ':include :type=code yaml')

Ваш тест должен читать `BASE_URL` и переходить по этому URL:

```python
import os

base_url = os.environ["BASE_URL"]
page.goto(base_url)
```

Для приватных репозиториев `actions/checkout` может checkout-ить репозиторий во время выполнения workflow. Важная часть здесь - сетевой доступ: браузер, запущенный в xClouds, не видит `localhost` внутри GitHub runner, поэтому туннель становится публичным маршрутом обратно к приложению под тестом.

## Частые ошибки

| Симптом | Вероятная причина | Как исправить |
| --- | --- | --- |
| `XCLOUDS_API_KEY is not set` | Repository secret отсутствует или недоступен для этого запуска workflow | Добавьте `XCLOUDS_API_KEY` в repository Actions secrets и перезапустите workflow |
| Workflow работает на `push`, но падает на pull request из fork | GitHub не передает большинство secrets в workflows, запущенные из forks | Запускайте smoke-тест на доверенных branches или используйте отдельную workflow policy для внешних PR |
| Удаленный браузер не может открыть `localhost:3000` | `localhost` указывает на окружение удаленного браузера, а не на GitHub Actions runner | Запустите xClouds dev tunnel и переходите по URL туннеля |
| URL туннеля не загружает приложение | Локальное приложение не готово, порт указан неверно или туннель стартовал раньше, чем сервер начал слушать | Сначала проверьте приложение локально в runner, затем запустите туннель с тем же портом |
| Playwright не может подключиться | Версия Python-клиента Playwright не совпадает с версией endpoint | Используйте `playwright==1.58.0` с endpoint `v1.58` или обновляйте оба значения вместе |
| Selenium не может создать сессию | Неверный WebDriver URL или API-ключ | Проверьте `http://selenium.xclouds.dev/wd/hub?api_key=...` и при необходимости ротируйте ключ |
| Job зависает после failed assertion | Браузерная сессия не была закрыта | Оставьте `browser.close()` или `driver.quit()` в блоке `finally` |
| Assertion по заголовку страницы падает | Целевая страница изменилась или не загрузилась | Начните с `https://example.com`, затем замените ее на URL вашего приложения после стабилизации smoke-теста |
| API-ключ появляется в logs | Ключ был напечатан или передан через аргумент команды | Передавайте ключ через `env` и никогда не печатайте endpoint URL с добавленным ключом |

## Production notes

- Храните API-ключи xClouds в GitHub Actions secrets или в secret store вашей организации.
- Учитывайте другое поведение для pull requests из forks, потому что GitHub скрывает от таких запусков большинство secrets.
- Загружайте screenshots, traces или logs как GitHub Actions artifacts только когда ваши тесты их создают. Не загружайте файлы, которые содержат secrets.
- Сначала используйте один небольшой smoke-тест. Добавляйте полные UI suites после того, как убедитесь, что удаленный endpoint, secrets и путь cleanup работают.
- Для тестов приватного UI открывайте наружу только CI-порт приложения, который нужен браузеру. Не маршрутизируйте admin-сервисы, базы данных или внутренние dashboards через туннель.
- Параллельные jobs могут запускать несколько удаленных браузерных сессий. Согласуйте job matrix и test sharding с concurrency, доступной на вашем аккаунте xClouds.
- Всегда закрывайте удаленные сессии после каждого тестового запуска, чтобы освобождать браузерную емкость.

## Источники

- [GitHub Actions secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
- [GitHub Actions Python CI](https://docs.github.com/actions/guides/building-and-testing-python)
- [GitHub Actions Node.js CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/building-and-testing-nodejs)
- [Playwright CI](https://playwright.dev/docs/ci)
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
