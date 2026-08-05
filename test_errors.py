from playwright.sync_api import sync_playwright

def get_console_errors():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        errors = []
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(str(err)))

        page.goto("http://localhost:8080/EFLTG.html")
        page.wait_for_timeout(2000)

        # Click fight
        try:
            page.locator("#btn-fight").click()
            page.wait_for_timeout(1000)
        except Exception as e:
            errors.append(str(e))

        print("ERRORS ENCOUNTERED:")
        for err in errors:
            print("-", err)

        browser.close()

if __name__ == "__main__":
    get_console_errors()
