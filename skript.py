import requests

BASE_URL = "https://www.sportovisteznojmo.cz"
PAGE_URL = f"{BASE_URL}/bazen-louka"

WIDGET_PREFIX = (
    "container-default-container2-feab2b38d137e5cea9200d3e3f11c19b-"
    "container-2componentContainer2_feab2b38d137e5cea9200d3e3f11c19b-"
    "widget-b1308b23b5d55aef9f10dc8070deaef5"
)

API_URL = f"{PAGE_URL}?{WIDGET_PREFIX}-method=getZoneDataJSON&do={WIDGET_PREFIX}-app"


def fetch_zone_data() -> dict:
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
        # 1. Získání čerstvé session / cookies
        session.get(PAGE_URL, timeout=15)
        # 2. Stažení JSON dat zóny
        response = session.get(API_URL, timeout=15)
        response.raise_for_status()
        return response.json()


if __name__ == "__main__":
    data = fetch_zone_data()
    print(data)
