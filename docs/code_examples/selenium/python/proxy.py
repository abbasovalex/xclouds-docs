# proxy_via_selenium.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType

XCLOUDS_URL = "https://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY"
PROXY_SERVER = "http://proxy.server.com:8080"  # You can use http://user:password@proxy.server.com:8080 also

options = ChromeOptions()
options.proxy = Proxy({
    "proxyType": ProxyType.MANUAL,
    "httpProxy": PROXY_SERVER,
    "sslProxy": PROXY_SERVER,
})

driver = webdriver.Remote(command_executor=XCLOUDS_URL, options=options)
driver.get("https://bin.xclouds.dev/ip")
print(driver.page_source)
driver.quit()