# Puppeteer And CDP Example

Use this example when you need a Chrome DevTools Protocol endpoint for Puppeteer, Playwright CDP workflows, or AI browser automation frameworks.

## Prerequisites

```bash
npm install puppeteer
```

## Puppeteer Connection

[puppeteer_connect.js](../../code_examples/puppeteer_cdp/javascript/puppeteer_connect.js ':include :type=code javascript')

Expected output:

```text
Page title: "Example Domain"
```

## Playwright Through CDP

[playwright_cdp_connect.js](../../code_examples/puppeteer_cdp/javascript/playwright_cdp_connect.js ':include :type=code javascript')

## browser-use Agent

[browser_use_agent.py](../../code_examples/puppeteer_cdp/python/browser_use_agent.py ':include :type=code python')

## Common Errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Puppeteer cannot connect | Wrong CDP endpoint | Use `wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY` |
| Authentication fails | API key is missing or wrong | Replace `YOUR_API_KEY` with your xClouds CDP key |
| CDP command fails | Command is not supported by the current browser context | Test with a simple `page.goto()` first |
| Agent does not run | Missing external LLM key | Set the key required by your agent framework |
| Session stays open | Browser was not closed | Call `await browser.close()` when the task finishes |

## Production Notes

CDP gives powerful browser control. Keep API keys private, isolate untrusted automation tasks, and close sessions when work is done.
