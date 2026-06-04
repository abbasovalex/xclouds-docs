# Selenium Example

Use this example when you already have Selenium tests and want to run them through the xClouds remote WebDriver endpoint.

## Prerequisites

- Python 3, Go, or PHP
- Selenium client library for your language
- An xClouds Selenium API key

For Python:

```bash
pip install selenium urllib3
```

For Go:

```bash
go get github.com/tebeka/selenium
```

For PHP:

```bash
composer require php-webdriver/webdriver
```

## Basic Connection

<!-- tabs:start -->

#### **Python**

[connect_to_xclouds.py](../../code_examples/selenium/python/connect_to_xclouds.py ':include :type=code python')

#### **Go**

[connect_to_xclouds.go](../../code_examples/selenium/go/connect_to_xclouds.go ':include :type=code go')

#### **PHP**

[connect_to_xclouds.php](../../code_examples/selenium/php/connect_to_xclouds.php ':include :type=code php')

<!-- tabs:end -->

Expected result:

```text
The script prints the page HTML returned by the remote browser.
```

## Choose Browser Settings

The source app example configures browser version, page load strategy, and platform.

[choose_browser.py](../../code_examples/selenium/python/choose_browser.py ':include :type=code python')

## Configure Chrome Options

[chrome_options.py](../../code_examples/selenium/python/chrome_options.py ':include :type=code python')

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
