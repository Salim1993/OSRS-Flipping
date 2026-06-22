import requests
from typing import Any

from src.domain.repositories import IPriceRepository

BASE_URL = "https://prices.runescape.wiki/api/v1/osrs"
HEADERS = {"User-Agent": "OSRS-Flip-Analyzer/1.0 - Learning Project"}


class OsrsApiClient(IPriceRepository):
    def get_mapping(self) -> list[dict]:
        """Fetch the full item id → name/metadata mapping."""
        response = requests.get(f"{BASE_URL}/mapping", headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_latest_prices(self) -> dict[str, Any]:
        """Fetch the most recent insta-buy/sell price for every traded item."""
        response = requests.get(f"{BASE_URL}/latest", headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()["data"]

    def get_hourly_prices(self) -> dict[str, Any]:
        """Fetch 1-hour average prices and trade volumes for every traded item."""
        response = requests.get(f"{BASE_URL}/1h", headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()["data"]
