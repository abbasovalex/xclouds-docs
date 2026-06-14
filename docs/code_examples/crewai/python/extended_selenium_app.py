import os
import argparse
import json
from pathlib import Path
from crewai import Agent, Crew, Task, LLM
from crewai.tools import tool


@tool
def cloud_browser(uri, cookies_path):
    """
    Fetch a page through the xclouds remote Selenium browser.
    Result will be extracted the HTML content from the page.
    This function return json result after all JavaScript code is executed on the page.
    """
    from selenium import webdriver
    from selenium.common.exceptions import WebDriverException
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from urllib3.exceptions import MaxRetryError

    try:
        cookies = Path(cookies_path)
        if not cookies.is_file():
            raise FileNotFoundError(f"Cookie file not found: {cookies_path}")

        cookies = json.loads(cookies.read_text(encoding="utf-8"))
        if not isinstance(cookies, list):
            raise ValueError("Cookie file must be an EditThisCookie-style JSON list.")

        XCLOUDS_API_KEY = os.environ.get("XCLOUDS_API_KEY", None)  # <- your api key here
        options = ChromeOptions()
        options.browser_version = "111.0"
        options.page_load_strategy = "normal"
        options.platform_name = "linux"
        options.add_argument("--start-maximized")
        options.add_argument("--no-first-run")
        options.add_experimental_option('excludeSwitches', ['load-extension', 'enable-automation', 'enable-logging'])

        driver = webdriver.Remote(command_executor=f"https://selenium.xclouds.dev/wd/hub?api_key={XCLOUDS_API_KEY}",
                                  options=options)
        driver.get(uri)
        for cookie in cookies:
            item = {
                "name": cookie["name"],
                "value": cookie["value"],
                "path": cookie.get("path", "/"),
                "domain": cookie.get("domain"),
                "secure": bool(cookie.get("secure", True)),
            }
            expiration = cookie.get("expirationDate") or cookie.get("expiry")
            if expiration:
                item["expiry"] = int(expiration)
            try:
                driver.add_cookie(item)
            except Exception as e:
                print(f"Error: {e}")
        driver.refresh()

        page_title = driver.title
        page_source = driver.page_source
        page_cookies = driver.get_cookies()
        driver.quit()
    except WebDriverException as e:
        print(f"Error: {e.msg}")
    except MaxRetryError as e:
        print(f"Host is unavailable")

    return json.dumps({
        'page_title': page_title,
        'page_body': page_source,
        'page_size': len(page_source.encode('utf-8')),
        'page_cookies': page_cookies
    })
cloud_browser.cache_function = False
cloud_browser.result_as_answer = True
cloud_browser.max_usage_count = 10


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", required=True)
    parser.add_argument("--cookies", help="path to file with json cookies")
    args = parser.parse_args()

    minimax2_5 = LLM(
        model="ollama/minimax-m2.5:cloud",
        api_key=os.environ.get("OLLAMA_API_KEY", None),  # <- your api key here
        base_url="http://localhost:11434"
    )

    web_agent = Agent(
        role="Web developer",
        goal="Investigate a site",
        backstory="You know html, css, javascript, etc",
        tools=[cloud_browser],
        llm=minimax2_5
    )

    visit_site = Task(
        description="Call cloud_browser tool with args {site_uri}, {cookies_path}",
        expected_output=(
            "A bulleted list containing the page title (get from tool result without changes), "
            "page size (get from tool result without changes) and your short description only"
        ),
        agent=web_agent
    )

    crew = Crew(agents=[web_agent], tasks=[visit_site], cache=False, verbose=True)

    result = crew.kickoff(inputs={"site_uri": args.uri, 'cookies_path': args.cookies})
    print(result.raw)
