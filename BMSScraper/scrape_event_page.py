# scrape_event_page.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

def scrape_event(event_url):
    with sync_playwright() as p:
        page = p.chromium.launch().new_page()
        page.goto(event_url)
        page.wait_for_timeout(4000)

        soup = BeautifulSoup(page.content(), "html.parser")

        description = soup.get_text(" ", strip=True)
        venue = soup.find("span", string=lambda x: x and "Venue" in x)

        return {
            "event_url": event_url,
            "description": description,
            "venue": venue.text if venue else None
        }
