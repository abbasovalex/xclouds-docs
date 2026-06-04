using Microsoft.Playwright;

using var playwright = await Playwright.CreateAsync();
var browser = await playwright.Firefox.ConnectAsync(
    "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
);
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");
await browser.CloseAsync();
