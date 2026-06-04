import { chromium } from 'playwright';

const browser = await chromium.connect({
  wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});

const context = await browser.newContext();

await context.addCookies([{
  name: 'session_id',
  value: 'demo-cookie-value',
  domain: 'xclouds.dev',
  path: '/',
}]);

const page = await context.newPage();
await page.goto('https://bin.xclouds.dev/cookies');

console.log(await page.textContent('body'));

await browser.close();
