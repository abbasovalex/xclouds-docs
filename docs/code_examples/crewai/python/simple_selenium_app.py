import os
import argparse
from pathlib import Path
from crewai import Agent, Crew, Task, LLM, Process
from crewai.tools import tool


@tool
def cloud_browser(uri):
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
        XCLOUDS_API_KEY = os.environ.get("XCLOUDS_API_KEY", None)  # <- your api key here
        driver = webdriver.Remote(command_executor=f"https://selenium.xclouds.dev/wd/hub?api_key={XCLOUDS_API_KEY}",
                                  options=ChromeOptions())
        driver.get(uri)
        page_title = driver.title
        page_source = driver.page_source
        driver.quit()
    except WebDriverException as e:
        print(f"Error: {e.msg}")
    except MaxRetryError as e:
        print(f"Host is unavailable")
    return {
        'page_title': page_title,
        'page_body': page_source,
        'page_size': len(page_source.encode('utf-8'))
    }
cloud_browser.cache_function = False


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", required=True)
    args = parser.parse_args()

    minimax2_5 = LLM(
        model="ollama/minimax-m2.5:cloud",
        api_key=os.environ.get("OLLAMA_API_KEY", None),  # <- your api key here
        base_url="http://localhost:11434"
    )

    web_agent = Agent(
        role="Experienced user",
        goal="Describe a site",
        backstory="",
        tools=[cloud_browser],
        llm=minimax2_5
    )

    visit_site = Task(
        description="Open {site_uri} site",
        expected_output=(
            "A bulleted list containing the page title (get from tool result without changes), "
            "page size (get from tool result without changes) and your short description only"
        ),
        agent=web_agent
    )

    crew = Crew(agents=[web_agent], tasks=[visit_site], cache=False)

    result = crew.kickoff(inputs={"site_uri": args.uri})
    print(result.raw)
