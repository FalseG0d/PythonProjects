# run_pipeline.py
import pandas as pd
from scrape_event_page import scrape_event
from capture_prices import capture_prices
from extract_hidden_costs import extract_hidden_costs

events = pd.read_csv("data/events.csv")

all_sessions = []

for _, row in events.iterrows():
    meta = scrape_event(row["event_url"])
    prices = capture_prices(row["event_url"])

    if not prices.empty:
        prices["event_url"] = row["event_url"]
        prices["hidden_cost_flags"] = extract_hidden_costs(meta["description"])
        all_sessions.append(prices)

final_df = pd.concat(all_sessions, ignore_index=True)
final_df.to_csv("data/sessions.csv", index=False)