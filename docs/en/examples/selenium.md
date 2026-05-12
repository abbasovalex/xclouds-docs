# Selenium Example

Use this example when you already have Selenium tests and want to run them through the xClouds remote WebDriver endpoint.

## Prerequisites

- Python 3
- Selenium installed
- An xClouds Selenium API key

```bash
pip install selenium urllib3
```

## Basic Connection

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

Expected result:

```text
The script prints the page HTML returned by the remote browser.
```

## Choose Browser Settings

The source app example configures browser version, page load strategy, and platform.

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

## Configure Chrome Options

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

## Common Errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `Host is unavailable` | Endpoint cannot be reached | Check network access and the endpoint URL |
| Authentication fails | API key is missing or wrong | Replace `YOUR_API_KEY` with your xClouds Selenium key |
| Session starts but page fails | Target site blocks or times out | Try a simpler URL such as `https://example.com` |
| Browser options are ignored | Unsupported capability | Start with the basic example, then add options one by one |
| Test hangs | `driver.quit()` was not reached | Use `try/finally` in production tests |

## Production Notes

Keep the API key in an environment variable or secret manager. Always close remote sessions after each test so browser capacity is released.
