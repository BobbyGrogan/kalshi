import json
import time
import requests
import os
from datetime import datetime

API_URL = "https://api.elections.kalshi.com/v1/events/"
DATA_DIR = "data"
FETCH_INTERVAL = 60  # Fetch data every 60 seconds


def fetch_api_data():
    """Fetch data from the Kalshi API."""
    print("Fetching event data from API...")
    params = {
        "single_event_per_series": "false",
        "tickers": "BTCETHRETURN-24DEC31,BTCMAX100-24,BTCMINY-24DEC31,ETHATH-24,ETHMINY-24DEC31,KXBTC-24NOV2217,KXBTCD-24NOV2117,KXBTCD-24NOV2217,KXBTCD-24NOV2217,KXBTCMAXW-24-NOV22,KXBTCMAXY-25,KXBTCRESERVE-26,KXCBVOLUME-Q4-24,KXCRYPTOREG-26,KXDOGE-24NOV2217,KXDOGED-24NOV2217,KXDOGEMAX1,KXDOGEMAX69-25,KXDOGEMAXW-24,KXDOGEMAXY-24,KXETH-24NOV2217,KXETHD-24NOV2217,KXETHMAXY-25DEC31,KXUSDTMIN-25DEC31",
        "page_size": 100,
        "page_number": 1,
    }
    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        print("Successfully fetched event data.")
        if "events" not in data:
            raise ValueError("Unexpected API response structure")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
    except ValueError as e:
        print(f"Data validation error: {e}")
    return None


def transform_data(response_data):
    """Transform the API response data into a smaller JSON structure."""
    print("Transforming event data...")
    small_json = {"events": []}
    if not response_data:
        print("No response data to transform.")
        return small_json

    for event in response_data.get("events", []):
        print(f"Processing event: {event.get('title', 'Unknown Title')} (Ticker: {event.get('ticker')})")
        small_event = {
            "ticker": event.get("ticker"),
            "title": event.get("title"),
            "category": event.get("category"),
            "target_datetime": event.get("target_datetime"),
            "settlement_details": event.get("settle_details"),
            "markets": [],
        }
        for market in event.get("markets", []):
            market_ticker = market.get("ticker_name")
            print(f"  Processing market: {market_ticker}")
            small_market = {
                "ticker_name": market_ticker,
                "status": market.get("status"),
                "open_date": market.get("open_date"),
                "close_date": market.get("close_date"),
                "expiration_date": market.get("expiration_date"),
                "yes_bid": market.get("yes_bid"),
                "yes_ask": market.get("yes_ask"),
                "last_price": market.get("last_price"),
                "volume": market.get("volume"),
                "open_interest": market.get("open_interest"),
                "dollar_volume": market.get("dollar_volume"),
                "yes_sub_title": market.get("yes_sub_title"),
                "no_sub_title": market.get("no_sub_title"),
            }
            small_event["markets"].append(small_market)
        small_json["events"].append(small_event)

    print("Event data transformation complete.")
    return small_json


def write_to_file(data, output_dir=DATA_DIR):
    """Save JSON data to a timestamped file and update index.json."""
    print("Saving data to file...")
    try:
        # Create the directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Create a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"events_{timestamp}.json")

        # Save the JSON data to the file
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Data written to {filename}")

        # Update index.json
        update_index(output_dir, filename)
    except Exception as e:
        print(f"Error writing to file: {e}")


def update_index(output_dir, new_file):
    """Update the index.json file with the new JSON file."""
    print("Updating index.json...")
    index_path = os.path.join(output_dir, "index.json")
    try:
        if os.path.exists(index_path):
            with open(index_path, "r") as index_file:
                index_data = json.load(index_file)
        else:
            index_data = []

        # Avoid duplicate entries
        new_file_basename = os.path.basename(new_file)
        if new_file_basename not in index_data:
            index_data.append(new_file_basename)

        # Write the updated index back to file
        with open(index_path, "w") as index_file:
            json.dump(index_data, index_file, indent=2)
        print(f"index.json updated with {new_file_basename}")
    except Exception as e:
        print(f"Error updating index.json: {e}")


def main():
    """Main loop to fetch, transform, and save data every interval."""
    while True:
        print("Starting data fetch cycle...")
        full_data = fetch_api_data()
        if full_data:
            print("Data fetched. Transforming...")
            small_data = transform_data(full_data)
            print("Saving transformed data...")
            write_to_file(small_data)
        else:
            print("No data fetched. Skipping this interval.")
        print(f"Cycle complete. Waiting for {FETCH_INTERVAL} seconds...\n")
        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Script terminated by user.")
