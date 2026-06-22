from dataclasses import dataclass
from typing import Optional


@dataclass
class Item:
    id: int
    name: str
    members: bool = False


@dataclass
class PriceData:
    item_id: int
    high: Optional[int]         # insta-buy price (what buyers pay)
    low: Optional[int]          # insta-sell price (what sellers receive)
    high_volume: Optional[int]  # hourly buy volume
    low_volume: Optional[int]   # hourly sell volume


@dataclass
class FlipOpportunity:
    item: Item
    buy_price: int      # estimated price to buy at (≈ low)
    sell_price: int     # estimated price to sell at (≈ high)
    tax: int            # GE tax on sale (1%, capped at 5M)
    profit: int         # profit per item after tax
    roi_percent: float  # return on investment as a percentage
    volume: int         # combined hourly trade volume
