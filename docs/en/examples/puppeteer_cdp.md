# Puppeteer And CDP Example

Use this example when you need a Chrome DevTools Protocol endpoint for Puppeteer, Playwright CDP workflows, or AI browser automation frameworks.

## Prerequisites

```bash
npm install puppeteer
```

## Puppeteer Connection

```javascript
import puppeteer from 'puppeteer';

const browser = await puppeteer.connect({
    browserWSEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY'
});

const page = await browser.newPage();

await page.goto('https://example.com');
const title = await page.title();
console.log(`Page title: "${title}"`);

await browser.close();
```

Expected output:

```text
Page title: "Example Domain"
```

## Playwright Through CDP

```javascript
import { chromium } from 'playwright';

const browser = await chromium.connect({
    wsEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY',
});

const page = await browser.newPage();
const client = await page.context().newCDPSession(page);
await client.send('Animation.enable');
client.on('Animation.animationCreated', () => console.log('Animation created!'));
const response = await client.send('Animation.getPlaybackRate');
console.log('playback rate is ' + response.playbackRate);
await client.send('Animation.setPlaybackRate', {
  playbackRate: response.playbackRate / 2
});
```

## browser-use Agent

```python
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

BROWSER_USE_API_KEY = 'your browser-use api key'

async def main():
    browser = Browser(cdp_url='wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY')
    agent = Agent(
        task='Visit https://habr.com/ and search for "vpn"',
        browser=browser,
        llm=ChatBrowserUse(api_key=BROWSER_USE_API_KEY),
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
```

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
