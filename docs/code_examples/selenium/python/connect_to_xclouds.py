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