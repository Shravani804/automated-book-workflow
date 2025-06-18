from playwright.sync_api import sync_playwright

def scrape_chapter():
    url = "https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1"

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Extract content from main content area
        content = page.inner_text("div#mw-content-text")

        # Save raw text
        with open("data/chapter1.txt", "w", encoding="utf-8") as f:
            f.write(content)

        # Save full-page screenshot
        page.screenshot(path="data/chapter1.png", full_page=True)

        browser.close()

if __name__ == "__main__":
    scrape_chapter()
