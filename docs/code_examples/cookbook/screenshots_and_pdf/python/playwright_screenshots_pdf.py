from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect(
        ws_endpoint='wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY'
    )
    page = browser.new_page()
    page.goto('https://example.com')

    png_bytes = page.screenshot()
    with open('screenshot.png', 'wb') as f:
        f.write(png_bytes)

    pdf_bytes = page.pdf(format='A4')
    with open('page.pdf', 'wb') as f:
        f.write(pdf_bytes)

    browser.close()
