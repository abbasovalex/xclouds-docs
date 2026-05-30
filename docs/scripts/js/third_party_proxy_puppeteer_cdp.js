import puppeteer from 'puppeteer';

const apiKey = process.env.XCLOUDS_CDP_API_KEY;
const proxyServer = process.env.EXTERNAL_PROXY_SERVER;
const mode = process.env.TARGET_URL ? 'advanced' : 'ip-check';
const targetUrl = process.env.TARGET_URL || 'https://ipinfo.io/ip';
const userAgent = process.env.USER_AGENT || [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  'AppleWebKit/537.36 (KHTML, like Gecko)',
  'Chrome/124.0.0.0 Safari/537.36',
].join(' ');
const cookies = process.env.COOKIE_JSON ? JSON.parse(process.env.COOKIE_JSON) : [];

if (!apiKey || !proxyServer) {
  throw new Error('Set XCLOUDS_CDP_API_KEY and EXTERNAL_PROXY_SERVER');
}

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', apiKey);
endpoint.searchParams.set('externalProxyServer', proxyServer);

const browser = await puppeteer.connect({
  browserWSEndpoint: endpoint.toString(),
});

try {
  const page = await browser.newPage();
  await page.setUserAgent(userAgent);
  await page.setExtraHTTPHeaders({
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
  });

  if (cookies.length > 0) {
    await page.setCookie(...cookies);
  }

  const response = await page.goto(targetUrl, {
    waitUntil: mode === 'ip-check' ? 'networkidle2' : 'domcontentloaded',
    timeout: 60000,
  });

  if (mode === 'ip-check') {
    const ip = (await page.$eval('body', element => element.innerText)).trim();
    if (!ip) {
      throw new Error('ipinfo.io returned an empty response');
    }
    console.log(`Proxy IP: ${ip}`);
  } else {
    console.log(`Status: ${response?.status() ?? 'unknown'}`);
    console.log(`Title: ${await page.title()}`);
  }
} finally {
  await browser.close();
}
