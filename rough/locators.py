from playwright.sync_api import sync_playwright

def test_locators():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,args=['--start-maximized'])
        context=browser.new_context(no_viewport=True)
        page=context.new_page()
