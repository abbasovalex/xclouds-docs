from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

driver = webdriver.Remote(
    command_executor=XCLOUDS_URL,
    options=ChromeOptions(),
)

try:
    driver.get("https://httpbin.org")

    driver.add_cookie({
        "name": "session_id",
        "value": "demo-cookie-value",
        "path": "/",
    })
    driver.refresh()

    driver.get("https://httpbin.org/cookies")
    print(driver.execute_script("return document.body.innerText"))
finally:
    driver.quit()
