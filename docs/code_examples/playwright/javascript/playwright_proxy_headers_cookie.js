// proxy_via_cdp_with_custom_headers_and_cookie.js
import { chromium } from 'playwright';

const endpoint = new URL('wss://cdp.xclouds.dev/cdp/');
endpoint.searchParams.set('api_key', 'YOUR_API_KEY');
endpoint.searchParams.set('externalProxyServer', 'http://user:password@proxy.server.com:8080');

const browser = await chromium.connectOverCDP(endpoint.toString());
const context = browser.contexts()[0] || await browser.newContext();

try {

  await context.setExtraHTTPHeaders({
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Upgrade-Insecure-Requests': '1',
  });
  // Добавляем cookies в браузер
  const cookies = JSON.parse('[{"name":"session_id","value":"demo","domain":".xclouds.dev","path":"/"}]');
  await context.addCookies(cookies);

  const page = await context.newPage();
  await page.setExtraHTTPHeaders({'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'});


  // Отображает список cookies которые получил от нашего приложения (при условии, что мы их верно передали)
  const response = await page.goto('https://bin.xclouds.dev/cookies');
  const data = await response.json();
  console.log(`Cookies: ${(JSON.stringify(data, null, 2))}`);

  // Отображает список заголовков которые наше приложение отправило
  const response2 = await page.goto('https://bin.xclouds.dev/headers');
  const data2 = await response2.json();
  console.log(`Headers: ${(JSON.stringify(data2, null, 2))}`);

} finally {
  await browser.close();
}
