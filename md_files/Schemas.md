
# 📊 Database Schemas: Kalshi & Polymarket

This document provides a concise overview of the two databases used for tracking prediction market data for the 2025 Masters Tournament.

---

## 🟢 Kalshi Dataset (`masters-tournament_kalshi.db`)
- **Purpose**: Historical market data for each player contract on Kalshi.
- **Tables**: Each table corresponds to a **player** in the Masters Tournament.
- **Table Schema**:
  - `id` (TEXT): Kalshi contract ID.
  - `market_name` (TEXT): Name of the market (typically the player's name).
  - `yes_price` (REAL): Price for "Yes" in USDC — range: 0.01 to 0.99. The price of betting yes on this player.
  - `no_price` (REAL): Price for "No" in USDC — range: 0.01 to 0.99. The price of betting no on this player.
  - `timestamp` (TEXT): ISO-formatted datetime when the data was scraped.

---

## 🟣 Polymarket Dataset (`num_2025_masters_winner_polymarket.db`)
- **Purpose**: Captures prediction market data from Polymarket for the same event.
- **Tables**: Each table corresponds to a **player** in the Masters Tournament.
- **Table Schema**:
  - `id` (INTEGER): Auto-incremented primary key.
  - `market_name` (TEXT): Name of the market (typically the player's name).
  - `yes_price` (REAL): Price for "Yes" in USDC — range: 0.01 to 0.99.
  - `no_price` (REAL): Price for "No" in USDC — range: 0.01 to 0.99.
  - `trading_volume` (REAL): Amount of volume traded in the market — varies by market.
  - `timestamp` (TEXT): ISO-formatted datetime when the data was scraped.
