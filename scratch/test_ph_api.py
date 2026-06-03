import time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
            if "graphql" in response.url.lower() or "search" in response.url.lower():
                try:
                    data = response.json()
                    print("Found JSON response from:", response.url)
                    # Just print keys to see structure
                    # print(data.keys())
                except:
                    pass

        page.on("response", handle_response)
        page.goto("https://www.producthunt.com/search?q=mental+health+ai")
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    run()
