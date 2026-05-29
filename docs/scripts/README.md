Run these scripts:

python3 python/httpbin_get_json.py
python3 python/httpbin_post_json.py
python3 python/httpbin_status_check.py

For GitHub Actions browser smoke tests, install the matching dependency and
provide an xClouds API key:

python3 -m pip install playwright==1.58.0
XCLOUDS_API_KEY=your_key python3 python/github_actions_playwright_smoke.py

python3 -m pip install selenium
XCLOUDS_API_KEY=your_key python3 python/github_actions_selenium_smoke.py
