from src.domain.models import Item, FlipOpportunity
from src.domain.repositories import IPriceRepository

GE_TAX_RATE = 0.01
GE_TAX_CAP = 5_000_000

MIN_VOLUME = 20       # ignore illiquid items (hard to buy/sell)
MIN_PROFIT = 500      # ignore items with negligible margins
MIN_BUY_PRICE = 100   # ignore near-worthless items with misleading ROI


def _calculate_tax(sell_price: int) -> int:
    return min(int(sell_price * GE_TAX_RATE), GE_TAX_CAP)


class FetchItemsUseCase:
    def __init__(self, client: IPriceRepository):
        self._client = client

    def execute(self) -> dict[int, Item]:
        mapping = self._client.get_mapping()
        return {
            entry["id"]: Item(
                id=entry["id"],
                name=entry["name"],
                members=entry.get("members", False),
            )
            for entry in mapping
        }


class AnalyzeFlipsUseCase:
    def __init__(self, client: IPriceRepository):
        self._client = client

    def execute(
        self,
        items: dict[int, Item],
        top_n: int = 20,
        sort_by: str = "profit",  # "profit" | "roi" | "volume"
    ) -> list[FlipOpportunity]:
        latest = self._client.get_latest_prices()
        hourly = self._client.get_hourly_prices()

        # Both APIs return string item IDs; int conversion is needed only for the
        # items dict lookup — keep item_id_str for hourly cross-reference.
        opportunities = []

        for item_id_str, price_info in latest.items():
            item_id = int(item_id_str)
            item = items.get(item_id)
            if item is None:
                continue

            high = price_info.get("high")  # insta-buy price (sell target)
            low = price_info.get("low")    # insta-sell price (buy price)
            if not high or not low or low < MIN_BUY_PRICE:
                continue

            hourly_info = hourly.get(item_id_str, {})
            volume = (hourly_info.get("highPriceVolume") or 0) + (hourly_info.get("lowPriceVolume") or 0)
            if volume < MIN_VOLUME:
                continue

            tax = _calculate_tax(high)
            profit = high - low - tax
            if profit < MIN_PROFIT:
                continue

            roi = (profit / low) * 100

            opportunities.append(FlipOpportunity(
                item=item,
                buy_price=low,
                sell_price=high,
                tax=tax,
                profit=profit,
                roi_percent=roi,
                volume=volume,
            ))

        sort_key = {
            "profit": lambda o: o.profit,
            "roi":    lambda o: o.roi_percent,
            "volume": lambda o: o.volume,
        }.get(sort_by, lambda o: o.profit)

        return sorted(opportunities, key=sort_key, reverse=True)[:top_n]
