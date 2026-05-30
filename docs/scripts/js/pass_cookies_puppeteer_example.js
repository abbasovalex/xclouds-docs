import puppeteer from 'puppeteer';

const browser = await puppeteer.connect({
  browserWSEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY',
});

const context = browser.defaultBrowserContext();

await context.setCookie({
  name: 'session_id',
  value: 'demo-cookie-value',
  domain: 'httpbin.org',
  path: '/',
});

const page = await context.newPage();
await page.goto('https://httpbin.org/cookies');

console.log(await page.$eval('body', element => element.innerText));

await browser.close();
