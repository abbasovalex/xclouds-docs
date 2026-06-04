import com.microsoft.playwright.*;
import java.nio.file.Paths;

try (Playwright playwright = Playwright.create()) {
    Browser browser = playwright.chromium().connect(
        "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
    );
    Page page = browser.newPage();
    page.navigate("https://example.com");

    page.screenshot(new Page.ScreenshotOptions()
        .setPath(Paths.get("screenshot.png")));

    page.pdf(new Page.PdfOptions()
        .setPath(Paths.get("page.pdf")));

    browser.close();
}
