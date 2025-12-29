# discover_events.py
from playwright.sync_api import sync_playwright
import pandas as pd
import time
import requests

BASE_URL = "https://in.bookmyshow.com/explore/workshops-national-capital-region-ncr"
BASE_EVENT_URL = "https://in.bookmyshow.com/api/le/v2/synopsis/primary-sessions/"

def discover_events():
    events = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(BASE_URL, timeout=60000)
        page.wait_for_timeout(5000)
        
        # # Scroll the page for a fixed duration to trigger lazy-loading of more events
        # SCROLL_DURATION = 120  # seconds
        # SCROLL_INTERVAL_MS = 1000  # milliseconds between scrolls

        # start = time.time()
        # while time.time() - start < SCROLL_DURATION:
        #     # scroll down by one viewport height
        #     page.evaluate("window.scrollBy(0, window.innerHeight);")
        #     page.wait_for_timeout(SCROLL_INTERVAL_MS)

        # # small pause to ensure any final content loads
        # page.wait_for_timeout(2000)

        # select anchor elements that use the target classname
        cards = page.query_selector_all("a.sc-133848s-11")
        print(f"Discovered {len(cards)} Links")

        for card in cards:
            event_url = card.get_attribute("href")
            event_id = event_url.split("/")[-1] if event_url else None
            
            if not event_id:
                continue

            event_api_url = BASE_EVENT_URL + event_id
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
            
            try:
                resp = requests.get(
                    event_api_url,
                    headers=headers
                    )
                status = resp.status_code

                print(f"API Status: {status} for {event_api_url}")

                if status == 200:
                    api_data = resp.json()
                else:
                    # print(f"API returned status {status} for {event_api_url}")
                    api_data = {"status": status}
            
            except Exception as exc:
                print(f"Failed to fetch {event_api_url}: {exc}")
                api_data = {"error": str(exc)}

            # append the API response and basic metadata to events
            events.append({
                "event_id": event_id,
                "event_url": event_url,
                "api": str(api_data)
            })

            # polite short pause between requests
            time.sleep(0.5)

        browser.close()
        # dispose request context
        try:
            request_context.dispose()
        except Exception:
            pass

    df = pd.DataFrame(events).drop_duplicates()
    df.to_csv("data/events.csv", index=False)
    print(f"Discovered {len(df)} events")

if __name__ == "__main__":
    discover_events()