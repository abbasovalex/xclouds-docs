# xClouds Overview

xClouds gives developers remote browser automation endpoints and a dev tunnel for local work.

Use it when you need one of these workflows:

- Run Selenium through a remote WebDriver endpoint.
- Connect Playwright to a remote browser over WebSocket.
- Connect Puppeteer, CDP tools, or AI browser agents to a remote Chrome DevTools Protocol endpoint.
- Expose a local app through a public HTTPS tunnel for webhooks, callbacks, demos, and browser tests.

## Endpoints

| Workflow | Endpoint |
| --- | --- |
| Selenium | `http://selenium.xclouds.dev/wd/hub?api_key=YOUR_API_KEY` |
| Playwright | `wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY` |
| Puppeteer / CDP | `wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY` |
| Dev tunnel | `xclouds tunnel start --authtoken YOUR_TUNNEL_TOKEN --port 8080` |

## Start Here

Pick the path that matches your task:

- [Dev tunnel](/en/examples/dev_tunnel): expose `localhost:8080` through a public HTTPS URL.
- [Selenium](/en/examples/selenium): connect Python Selenium to xClouds.
- [Playwright](/en/examples/playwright): connect Node.js, Python, Java, or C# Playwright.
- [Puppeteer and CDP](/en/examples/puppeteer_cdp): connect Puppeteer, Playwright CDP, or browser-use.

## Keep Your Keys Private

The examples use `YOUR_API_KEY` and `YOUR_TUNNEL_TOKEN`. Replace them with values from your xClouds account, and do not commit real keys to Git.
