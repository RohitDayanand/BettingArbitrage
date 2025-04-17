
# 📄 Polymarket Web Scraper Documentation

## Overview
This backend script scrapes prediction market data from Polymarket using Selenium and logs it into a SQLite database. It handles dynamic content loading, retry logic, element freshness, and scheduled scraping intervals.

---

## 📌 Table of Contents
- [Authentication](#authentication)
- [Execution Context](#execution-context)
- [Logic Flow](#logic-flow)
- [Helper Functions](#helper-functions)
- [Resource Management](#resource-management)
- [Error Handling](#error-handling)
- [Pitfalls & Best Practices](#pitfalls--best-practices)

---

## 🔐 Authentication
There is **no authentication layer** as the scraper operates on publicly accessible market data from Polymarket. No API keys or credentials are required.

---

## 🧠 Execution Context

### Entry Point
```python
if __name__ == "__main__":
    main()
```

### CLI Usage
```bash
python script.py <event_url> <iterations>
```
- `event_url`: URL of the Polymarket event.
- `iterations`: Number of refresh intervals to scrape data (~30s interval).

A **batch file** (`.bat`) is used to repeatedly launch the scraper, making it restartable and resilient to failures or timeouts.
- Batch script example:
  ```batch
  @echo off
  cd /d "C:\Users\student\Downloads\BettingArbitrage-main"
  C:\Users\student\AppData\Local\Programs\Python\Python313\python
  exe polymarket_scraper.py https://polymarket.com/event
  2025-masters-winner 9999
  pause
  ```
- This script is meant to be run continuously over long periods to gather time-series data.
- Change the location of the scraper and the python.exe to the folder that these files reside in your computer.

---

## 🧩 Logic Flow

### `main()`
- Parses CLI arguments.
- Initializes a headless Chrome WebDriver with anti-detection settings.
- Launches `polymarket_scraper`.

---

### `polymarket_scraper(event_url, event_id, iterations, driver)`
- Manages iterative scraping with refresh intervals.
- Refreshes browser every 3rd iteration.
- Implements timeout handling and browser reinitialization.

---

### `scrape_polymarket(url, event_id, table_created, driver)`
- Loads market page via Selenium.
- Waits for DOM elements using `WebDriverWait`.
- Extracts event name and market details:
  - Market name
  - Yes/No prices
  - Trading volume
- Converts and normalizes data.
- Writes data to a SQLite database.

---

## 🛠️ Helper Functions

### `standardizeColumnNames`
Imported from external module `standardize_names`, it is used to:
- Convert market/event names into SQLite-compliant table names.
- Normalize strings for consistency across entries.

---

## 💾 Resource Management

- **SQLite3** is used for persistent storage.
- Tables are dynamically created per market with the following schema:

```sql
CREATE TABLE IF NOT EXISTS <market_name> (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_name TEXT,
    trading_volume TEXT,
    yes_price REAL,
    no_price REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

- **Database filename**: `<event_id>_polymarket.db`

- **Webdriver**:
  - Headless Chrome with automation controls disabled.
  - Image loading disabled for performance.
  - Automatically re-instantiated on timeout.

---

## ⚠️ Error Handling

- **Try-Except Blocks**:
  - Protects Selenium operations (DOM lookups, page loading).
  - Handles common Selenium exceptions:
    - `NoSuchElementException`
    - `StaleElementReferenceException`
    - `ElementNotInteractableException`
    - `ReadTimeoutError`

- **Fallback Behaviors**:
  - Quits and restarts WebDriver on timeout.
  - Skips and retries on stale DOM elements.

---

## 🪤 Pitfalls & Best Practices

### ✅ What to Do
- **Use Headless Mode** for CI or server execution.
- **Sanitize Strings** using `standardizeColumnNames` to avoid SQL injection or malformed table names.
- **Wait for Elements** using `WebDriverWait` to ensure the DOM is fully loaded.

### ❌ What to Avoid
- **Too Many Iterations**: Avoid exceeding practical limits (`>9999`) to prevent browser crashes or system overloads.
- **Skipping Error Checks**: Always handle `ValueError` and `IndexError` during input parsing.
- **Using Raw Strings** for SQLite table names: always sanitize.

---

## 🔄 Future Improvements
- Add logging to file instead of stdout.
- Modularize the WebDriver setup.
- Use environment configs for scraping intervals and DB paths.
- Implement retry decorators for flaky network/element failures.
- Add test cases for CLI input and HTML parsing.

---
