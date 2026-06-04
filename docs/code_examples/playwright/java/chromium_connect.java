import com.microsoft.playwright.*;

public class Main {
    public static void main(String[] args) {
        try (Playwright playwright = Playwright.create()) {
            Browser browser = playwright.chromium().connect(
                "wss://playwright.xclouds.dev/v1.58/?api_key=YOUR_API_KEY"
            );
            Page page = browser.newPage();
            page.navigate("https://example.com");
            browser.close();
        }
    }
}
