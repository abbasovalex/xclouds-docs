// proxy_via_cdp.js
import puppeteer from 'puppeteer';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'https://user:password@proxy.server.com:8433');

const browser = await puppeteer.connect({
  browserWSEndpoint: endpoint.toString(),
});

try {
  const page = await browser.newPage();
  const response = await page.goto('https://bin.xclouds.dev/ip');
  const data = await response.json();
  console.log(`Proxy IP: ${data.origin}`);
} finally {
  await browser.close();
}
