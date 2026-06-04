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

[connect_to_xclouds.py](../../code_examples/selenium/python/connect_to_xclouds.py ':include :type=code python')

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
