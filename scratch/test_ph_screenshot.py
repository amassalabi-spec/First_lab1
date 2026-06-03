import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.producthunt.com/search?q=mental+health+ai", wait_until="networkidle", timeout=30000)
        time.sleep(3)
        page.screenshot(path="ph_test.png")
        print("Screenshot saved.")
        browser.close()

if __name__ == "__main__":
    run()
