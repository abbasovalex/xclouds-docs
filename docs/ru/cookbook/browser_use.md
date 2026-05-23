# Пример подключения через Browser Use


<!-- tabs:start -->
#### **python**

```python
import asyncio
from browser_use import Agent, Browser, ChatBrowserUse

BROWSER_USE_API_KEY = 'your browser-use api key'

async def main():
    browser = Browser(cdp_url='wss://cdp.xclouds.dev/cdp/?api_key=YOUR_API_KEY')
    agent = Agent(
        task='Visit https://habr.com/ and search for "vpn"',
        browser=browser,
        llm=ChatBrowserUse(api_key=BROWSER_USE_API_KEY),
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
```
<!-- tabs:end -->