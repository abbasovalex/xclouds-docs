from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect(
        ws_endpoint='wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY'
    )
    page = browser.new_page()
    page.goto('https://example.com')
    browser.close()
