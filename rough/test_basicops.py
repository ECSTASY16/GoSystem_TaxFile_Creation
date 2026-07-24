from playwright.sync_api import sync_playwright

def test_browseroperations():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,args=['--start-maximized'])
        context=browser.new_context(no_viewport=True)
        page=context.new_page()
        page.goto("https://demoqa.com/browser-windows")



        with page.expect_popup() as window:
            page.locator("#windowButton").click()
            new_window = window.value
            new_window.wait_for_load_state("domcontentloaded")
            print(new_window.url)
            heading=new_window.locator('#sampleHeading').inner_text()
            print(heading)
            new_window.close()
            page.close()

def test_loopthroughalllinks():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=['--start-maximized'])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        page.goto("https://demoqa.com/books")

        books = []

        rows = page.locator("table tbody tr")

        for i in range(rows.count()):
            cells = rows.nth(i).locator("td")

            book = {
                "Title": cells.nth(1).inner_text(),
                "Author": cells.nth(2).inner_text(),
                "Publisher": cells.nth(3).inner_text()
            }

            books.append(book)

        print(books)