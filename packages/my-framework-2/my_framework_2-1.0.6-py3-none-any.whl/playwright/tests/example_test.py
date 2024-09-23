from playwright.sync_api import sync_playwright

def test_example_page(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        title = page.title()
        print(f"Page title: {title}")
        if title == "Tricon Infotech":
            print("Test Passed")
        else:
            print("Test Failed")
        browser.close()

if __name__ == "__main__":
    test_example_page("https://www.triconinfotech.com/")
