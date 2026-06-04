import { chromium } from 'playwright';
import fs from 'fs';

const browser = await chromium.connect({
    wsEndpoint: 'wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY',
});
const page = await browser.newPage();
await page.goto('https://example.com');

const pngBuffer = await page.screenshot();
fs.writeFileSync('screenshot.png', pngBuffer);

const pdfBuffer = await page.pdf({ format: 'A4' });
fs.writeFileSync('page.pdf', pdfBuffer);

await browser.close();
