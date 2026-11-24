import csv
import json
import os
import re
from datetime import datetime, timezone
import requests

BASE_URL = "https://www.sportovisteznojmo.cz"
PAGE_URL = f"{BASE_URL}/bazen-louka"

WIDGET_PREFIX = (
    "container-default-container2-feab2b38d137e5cea9200d3e3f11c19b-"
    "container-2componentContainer2_feab2b38d137e5cea9200d3e3f11c19b-"
    "widget-b1308b23b5d55aef9f10dc8070deaef5"
)
API_URL = f"{PAGE_URL}?{WIDGET_PREFIX}-method=getZoneDataJSON&do={WIDGET_PREFIX}-app"
CSV_FILE = "wellness_history.csv"


def fetch_zone_data() -> dict | list | int | str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/157.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "cs,en;q=0.9,cs-CZ;q=0.8",
        "Referer": PAGE_URL,
        "X-Requested-With": "XMLHttpRequest",
    }

    with requests.Session() as session:
        session.headers.update(headers)
        session.get(PAGE_URL, timeout=15)
        response = session.get(API_URL, timeout=15)
        response.raise_for_status()
        return response.json()
# note

def extract_number_key(payload) -> str:
    """Extracts the value associated with the 'number' key inside the JSON payload."""
    def walk(obj):
        if isinstance(obj, dict):
            if "number" in obj and obj["number"] is not None:
                val = obj["number"]
                if isinstance(val, (int, float)):
                    return str(val)
                match = re.search(r"-?\d+", str(val))
                if match:
                    return match.group(0)
            for v in obj.values():
                found = walk(v)
                if found is not None:
                    return found
        elif isinstance(obj, list):
            for item in obj:
                found = walk(item)
                if found is not None:
                    return found
        return None

    found = walk(payload)
    return found if found is not None else ""


def append_to_csv(capacity_left: str, raw_payload) -> None:
    file_exists = os.path.exists(CSV_FILE)
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp_utc", "capacity_left", "raw_json"])
        writer.writerow([timestamp, capacity_left, json.dumps(raw_payload, ensure_ascii=False)])


if __name__ == "__main__":
    data = fetch_zone_data()
    capacity_left = extract_number_key(data)
    append_to_csv(capacity_left, data)
    print(f"Saved capacity_left={capacity_left} to {CSV_FILE}")
