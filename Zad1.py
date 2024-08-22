from playwright.sync_api import sync_playwright, expect, TimeoutError
import pytest


@pytest.fixture(scope='function')
def browser_context():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        yield context
        context.close()
        browser.close()


def test_login_and_add_to_cart(browser_context):
    page = browser_context.new_page()

    page.goto("https://bstackdemo.com/")

    page.click('text=Sign In')

    page.click('#username .css-1hwfws3')
    page.click('div[id^="react-select-2-option-0-0"]')

    page.click('#password .css-1hwfws3')
    page.click('div[id^="react-select-3-option-0-0"]')

    page.click('id=login-btn')

    page.wait_for_load_state('networkidle')

    add_to_cart_button = page.locator('text=Add to cart').first
    add_to_cart_button.click(timeout=5000)

    page.click('text=Cart')

    try:
        page.wait_for_selector('p.desc', timeout=30000)

        cart_items = page.locator('p.desc')
        quantity_found = cart_items.count() > 0

        if quantity_found:
            cart_items.first.screenshot(path="cart_item_screenshot.png")
            print(f"Screenshot of the cart item saved as 'cart_item_screenshot.png'")
        else:
            print("No item with quantity found in the cart")

        assert quantity_found, "No item with quantity found in the cart"

    except TimeoutError as e:
        print("Cart items not found within the timeout period")
        raise e

    page.click('text=Logout')

    page.wait_for_load_state('networkidle')

    page.close()


if __name__ == "__main__":
    pytest.main(["-v", "Zadanie1.py"])
