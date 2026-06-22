# OSRS Flip Analyzer

A Python tool that fetches live Grand Exchange prices from the OSRS Wiki API and identifies the best items to flip for profit.

---

## File Structure

```
RuneScape Flipping/
├── main.py                               # Entry point — runs the full analysis
├── requirements.txt                      # Python dependencies
└── src/
    ├── domain/
    │   └── models.py                     # Data models: Item, PriceData, FlipOpportunity
    ├── infrastructure/
    │   └── osrs_api_client.py            # Calls the OSRS Wiki Prices API
    ├── application/
    │   └── use_cases.py                  # Business logic: fetch items, analyze flips
    └── presentation/
        └── cli.py                        # Formats and prints the results table
```

The project follows **Clean Architecture** — each layer has a single responsibility and only depends on layers inward (presentation → application → domain).

---

## How to Run

**1. Install dependencies**
```
pip install -r requirements.txt
```

**2. Run the analyzer**
```
python main.py
```

The tool will fetch live prices and print a ranked table of the top 20 flip opportunities to your terminal.

---

## How Flipping Works

Flipping means buying an item cheap and selling it for more on the Grand Exchange (GE).

### The Spread

Every item on the GE has two prices at any moment:

| Price | API field | What it means |
|-------|-----------|---------------|
| **Buy price** | `low` | The insta-sell price — what buyers are currently offering |
| **Sell price** | `high` | The insta-buy price — what sellers are currently asking |

The gap between them is called the **spread**. Your profit comes from capturing that spread.

### The Math

```
tax    = sell_price × 1%   (capped at 5,000,000 gp)
profit = sell_price − buy_price − tax
ROI %  = (profit / buy_price) × 100
```

**Example — Dragon bones:**
```
Buy price:   2,100 gp
Sell price:  2,400 gp
Tax:            24 gp   (2,400 × 1%)
Profit:        276 gp   (2,400 − 2,100 − 24)
ROI:         13.1%      (276 / 2,100)
```

### Filters Applied

Not every item with a spread is worth flipping. The analyzer removes:

| Filter | Threshold | Reason |
|--------|-----------|--------|
| Min volume | 20 trades/hour | Low-volume items are hard to buy or sell |
| Min profit | 500 gp/item | Tiny margins aren't worth your time |
| Min buy price | 100 gp | Very cheap items can have misleading ROI |

Remaining opportunities are ranked by **profit per item** (highest first).

### Key Risks

- **Price manipulation** — some items have artificial spreads set by other players.
- **Buy limits** — each item has a GE buy limit per 4 hours, capping how much you can flip.
- **Slow fills** — your offer may sit unfilled if the market moves against you.
