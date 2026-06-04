import { firefox } from 'playwright';

const browser = await firefox.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');
await browser.close();
