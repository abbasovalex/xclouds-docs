import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

XCLOUDS_URL = "http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"

def load_cookies_from_file(driver, cookie_path):
    if not cookie_path.exists():
        raise FileNotFoundError(f"Cookie file not found: {cookie_path}")

    cookies = json.loads(cookie_path.read_text(encoding="utf-8"))
    if not isinstance(cookies, list):
        raise ValueError("Cookie file must be an EditThisCookie-style JSON list.")

    for cookie in cookies:
        item = {
            "name": cookie["name"],
            "value": cookie["value"],
            "path": cookie.get("path", "/"),
            "domain": cookie.get("domain"),
            "secure": bool(cookie.get("secure", True)),
        }
        expiration = cookie.get("expirationDate") or cookie.get("expiry")
        if expiration:
            item["expiry"] = int(expiration)
        driver.add_cookie(item)


driver = webdriver.Remote(
    command_executor=XCLOUDS_URL,
    options=ChromeOptions(),
)

try:
    driver.get("https://bin.xclouds.dev")
    load_cookies_from_file(driver, '~/my_cookies.json')
    driver.refresh()

    driver.get("https://bin.xclouds.dev/cookies")
    print(driver.execute_script("return document.body.innerText"))
finally:
    driver.quit()
