# GitHub Actions CI With xClouds

xClouds can run browser sessions for CI through remote Playwright and Selenium endpoints. Use this guide when you want GitHub Actions to execute a browser smoke test without maintaining Selenium Grid, browser drivers, or browser nodes inside the runner.

## Decision Context

- **Problem:** CI browser tests need browsers, drivers, and infrastructure. Teams often maintain Selenium Grid or install browser dependencies in every runner.
- **Decision:** Use xClouds when GitHub Actions should call a remote browser endpoint instead of managing browser nodes in CI.
- **Fit:** xClouds exposes Playwright WebSocket and Selenium WebDriver endpoints with API-key authentication.
- **Proof:** Two smoke scripts connect to xClouds, open `https://example.com`, check the page title, and exit non-zero if the remote browser did not work.

## Who This Is For

This page is for QA engineers, developers, and DevOps engineers who already run tests in GitHub Actions and want to move browser execution to xClouds.

## What You Will Build

You will add one GitHub Actions workflow with two independent jobs:

- `playwright-smoke` connects to `wss://playwright.xclouds.dev/v1.58/`.
- `selenium-smoke` connects to `http://selenium.xclouds.dev/wd/hub`.

Each job reads the same `XCLOUDS_API_KEY` secret and runs one self-validating Python script.

## Prerequisites

- An xClouds account and API key.
- A GitHub repository where you can add Actions secrets.
- Python tests, or a repository where a Python smoke script is acceptable.

## 1. Add The GitHub Secret

In your GitHub repository, open **Settings → Secrets and variables → Actions → New repository secret**.

Create a secret named:

```text
XCLOUDS_API_KEY
```

Use your xClouds API key as the value.

The workflow passes this secret through the `env` block. Do not put the API key directly into the workflow file or into a command-line argument.

## 2. Add The Smoke Scripts

Copy these scripts into your repository:

- [github_actions_playwright_smoke.py](/scripts/python/github_actions_playwright_smoke.py)
- [github_actions_selenium_smoke.py](/scripts/python/github_actions_selenium_smoke.py)

This guide assumes you put them here:

```text
scripts/xclouds/github_actions_playwright_smoke.py
scripts/xclouds/github_actions_selenium_smoke.py
```

If you use a different path, update the workflow commands in the next step.

## 3. Add The GitHub Actions Workflow

Create `.github/workflows/xclouds-browser-tests.yml`:

```yaml
name: xClouds browser tests

on:
  push:
  pull_request:

jobs:
  playwright-smoke:
    name: Playwright remote browser smoke
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: python -m pip install playwright==1.58.0

      - name: Run Playwright smoke test
        env:
          XCLOUDS_API_KEY: ${{ secrets.XCLOUDS_API_KEY }}
        run: python scripts/xclouds/github_actions_playwright_smoke.py

  selenium-smoke:
    name: Selenium remote browser smoke
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6

      - uses: actions/setup-python@v6
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: python -m pip install selenium

      - name: Run Selenium smoke test
        env:
          XCLOUDS_API_KEY: ${{ secrets.XCLOUDS_API_KEY }}
        run: python scripts/xclouds/github_actions_selenium_smoke.py
```

The jobs are separate so a Playwright failure and a Selenium failure are easy to read in the Actions UI.

## 4. Verify The Run

Push a branch or open a pull request. The workflow should show two successful jobs.

Expected Playwright output:

```text
xClouds Playwright smoke test passed
```

Expected Selenium output:

```text
xClouds Selenium smoke test passed
```

You can also run the scripts locally before committing them:

```bash
cd /path/to/your/repository
XCLOUDS_API_KEY=your_key python scripts/xclouds/github_actions_playwright_smoke.py
XCLOUDS_API_KEY=your_key python scripts/xclouds/github_actions_selenium_smoke.py
```

## Testing A Private UI In CI

The smoke scripts above open a public page. If your repository is private and your tests need to open your own UI, the remote xClouds browser needs a public HTTPS URL for the app running inside GitHub Actions.

Use the xClouds dev tunnel for that path:

1. Start your app in the GitHub Actions runner, for example on port `3000`.
2. Start `xclouds tunnel start --authtoken ... --port 3000`.
3. Pass your xClouds tunnel URL to the test as `BASE_URL`.
4. Make Playwright or Selenium open `BASE_URL`, not `localhost`.

Add two more secrets or variables:

| Name | Type | Purpose |
| --- | --- | --- |
| `XCLOUDS_TUNNEL_TOKEN` | Secret | Token used by the xClouds CLI to start the dev tunnel |
| `XCLOUDS_TUNNEL_URL` | Repository variable or secret | Your assigned tunnel URL, for example `https://your-subdomain.tunnel.xclouds.dev` |

Example job shape:

```yaml
ui-tests:
  name: Private UI tests through xClouds tunnel
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v6

    - uses: actions/setup-node@v6
      with:
        node-version: "24"

    - uses: actions/setup-python@v6
      with:
        python-version: "3.12"

    - name: Install app dependencies
      run: npm ci

    - name: Build app
      run: npm run build

    - name: Start app
      run: npm run start -- --host 127.0.0.1 --port 3000 &

    - name: Install xClouds CLI
      run: |
        # Download the Linux xClouds CLI archive from the xClouds app.
        # Then extract it and put the xclouds binary on PATH.
        chmod +x ./xclouds

    - name: Start xClouds tunnel
      env:
        XCLOUDS_TUNNEL_TOKEN: ${{ secrets.XCLOUDS_TUNNEL_TOKEN }}
      run: xclouds tunnel start --authtoken "$XCLOUDS_TUNNEL_TOKEN" --port 3000 &

    - name: Run UI tests
      env:
        XCLOUDS_API_KEY: ${{ secrets.XCLOUDS_API_KEY }}
        BASE_URL: ${{ vars.XCLOUDS_TUNNEL_URL }}
      run: python scripts/xclouds/run_ui_tests.py
```

Your test should read `BASE_URL` and navigate to that URL:

```python
import os

base_url = os.environ["BASE_URL"]
page.goto(base_url)
```

For private repositories, `actions/checkout` can check out the repository during the workflow run. The important part is network access: a browser running in xClouds cannot see `localhost` inside the GitHub runner, so the tunnel becomes the public route back to the app under test.

## Common Errors

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `XCLOUDS_API_KEY is not set` | The repository secret is missing or unavailable to this workflow run | Add `XCLOUDS_API_KEY` under repository Actions secrets and rerun the workflow |
| The workflow works on `push` but fails on a pull request from a fork | GitHub does not pass most secrets to workflows triggered from forks | Run the smoke test on trusted branches, or use a separate workflow policy for external PRs |
| The remote browser cannot open `localhost:3000` | `localhost` points at the remote browser environment, not the GitHub Actions runner | Start an xClouds dev tunnel and navigate to the tunnel URL |
| The tunnel URL does not load the app | The local app is not ready, the port is wrong, or the tunnel started before the server was listening | Check the app locally in the runner first, then start the tunnel with the same port |
| Playwright cannot connect | The Python Playwright client version does not match the endpoint version | Keep `playwright==1.58.0` with the `v1.58` endpoint, or update both together |
| Selenium cannot create a session | The WebDriver URL or API key is wrong | Check `http://selenium.xclouds.dev/wd/hub?api_key=...` and rotate the key if needed |
| The job hangs after a failed assertion | The browser session was not closed | Keep `browser.close()` or `driver.quit()` in a `finally` block |
| The page title assertion fails | The target page changed or did not load | Start with `https://example.com`, then replace it with your app URL after the smoke test is stable |
| The API key appears in logs | The key was printed or passed through a command argument | Pass the key through `env` and never print the endpoint URL with the key attached |

## Production Notes

- Keep xClouds API keys in GitHub Actions secrets or your organization secret store.
- Expect different behavior for forked pull requests because GitHub withholds most secrets from those runs.
- Upload screenshots, traces, or logs as GitHub Actions artifacts only when your tests create them. Do not upload files that contain secrets.
- Use one small smoke test first. Add full UI suites after you know the remote endpoint, secrets, and cleanup path work.
- For private UI tests, expose only the CI app port that the browser needs. Do not route admin services, databases, or internal dashboards through the tunnel.
- Parallel jobs can start multiple remote browser sessions. Match your job matrix and test sharding to the xClouds concurrency available on your account.
- Always close remote sessions after each test run so browser capacity is released.

## Sources

- [GitHub Actions secrets](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions)
- [GitHub Actions Python CI](https://docs.github.com/actions/guides/building-and-testing-python)
- [GitHub Actions Node.js CI](https://docs.github.com/en/actions/tutorials/build-and-test-code/building-and-testing-nodejs)
- [Playwright CI](https://playwright.dev/docs/ci)
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
