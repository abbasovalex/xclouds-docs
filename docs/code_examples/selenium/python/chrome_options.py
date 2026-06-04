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
