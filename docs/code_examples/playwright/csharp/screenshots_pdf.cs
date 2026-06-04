using Microsoft.Playwright;

using var playwright = await Playwright.CreateAsync();
var browser = await playwright.Chromium.ConnectAsync(
    "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
);
var page = await browser.NewPageAsync();
await page.GotoAsync("https://example.com");

await page.ScreenshotAsync(new PageScreenshotOptions { Path = "screenshot.png" });
await page.PdfAsync(new PagePdfOptions { Path = "page.pdf" });

await browser.CloseAsync();
