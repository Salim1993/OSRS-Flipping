# Project TODO

---

## Database

- [ ] Choose a database (SQLite for local dev, PostgreSQL for production)
- [ ] Design schema: `items`, `price_snapshots`, `flip_opportunities`
- [ ] Store every API response as a price snapshot with a timestamp
- [ ] Add a repository layer so use cases can query historical data, not just live prices
- [ ] Set up a scheduled job to fetch and save prices every hour automatically

---

## AI / Flip Analysis

- [ ] Add buy limit data per item (GE limits trades to N items per 4 hours — affects max profit)
- [ ] Calculate price volatility (std deviation over recent snapshots) as a risk score
- [ ] Add trend detection — is this item's price rising, falling, or stable over the last 24h?
- [ ] Build a composite flip score: weights profit, ROI, volume, trend, and risk together
- [ ] Train a simple ML model (linear regression or random forest) to predict which items
      will have a higher price in 1 hour based on historical patterns
- [ ] Add anomaly detection to flag items with unusual price spikes (possible manipulation)

---

## Website / Frontend

- [ ] Set up a FastAPI or Flask backend to serve flip data as a REST API
- [ ] Build a simple frontend dashboard (React or plain HTML/JS) to display opportunities
- [ ] Add a price history chart per item (line chart of high/low over time)
- [ ] Add filters on the frontend: members/F2P, min profit, min ROI, sort column
- [ ] Set up auto-refresh so the page updates with new prices without a manual reload

---

## Code & Infrastructure

- [ ] Create `src/domain/repositories.py` interface for the database layer (mirrors IPriceRepository) ✓ done
- [ ] Write unit tests for use case logic (mock the repository)
- [ ] Add a config file or `.env` support for filter thresholds (MIN_PROFIT, MIN_VOLUME, etc.)
- [ ] Add logging so price fetch errors are recorded, not just printed
- [ ] Package the project so it can be run as `osrs-flip` from the command line
- [ ] Find other tests we can setup
