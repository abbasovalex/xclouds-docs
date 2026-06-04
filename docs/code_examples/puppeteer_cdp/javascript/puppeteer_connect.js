import puppeteer from 'puppeteer';

const browser = await puppeteer.connect({
    browserWSEndpoint: 'wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY'
});

const page = await browser.newPage();

await page.goto('https://example.com');
const title = await page.title();
console.log(`Page title: "${title}"`);

await browser.close();
