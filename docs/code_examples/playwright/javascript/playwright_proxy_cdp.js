// proxy_via_cdp.js
import { chromium } from 'playwright';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'http://user:password@proxy.server.com:8080');

const browser = await chromium.connectOverCDP(endpoint.toString());

try {
  const context = browser.contexts()[0] || await browser.newContext();
  const page = await context.newPage();
  const response = await page.goto('https://bin.xclouds.dev/ip');
  const data = await response.json();
  console.log(`Proxy IP: ${data.origin}`);
} finally {
  await browser.close();
}
