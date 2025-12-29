# capture_prices.py
from playwright.sync_api import sync_playwright
import pandas as pd

def capture_prices(event_url):
    price_rows = []

    def handle_response(response):
        if "price" in response.url.lower():
            try:
                data = response.json()
                for ticket in data.get("tickets", []):
                    price_rows.append({
                        "ticket_type": ticket["name"],
                        "price": ticket["price"],
                        "convenience_fee": ticket.get("fee", 0),
                        "gst": ticket.get("gst", 0),
                        "final_price": ticket["price"] + ticket.get("fee", 0)
                    })
            except:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.on("response", handle_response)
        page.goto(event_url)
        page.wait_for_timeout(8000)
        browser.close()

    return pd.DataFrame(price_rows)