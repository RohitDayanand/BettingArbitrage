
# 📄 Kalshi Web Scraper Documentation

## Overview
This backend script scrapes prediction market data from Kalshi using Selenium and logs it into a SQLite database. It handles dynamic content loading, retry logic, element freshness, and scheduled scraping intervals.

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
---

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
- `event_url`: URL of the Kalshi event.
- `iterations`: Number of refresh intervals to scrape data (~30s interval).

A **batch file** (`.bat`) is used to repeatedly launch the scraper, making it restartable and resilient to failures or timeouts.
- Batch script example:
  ```batch
  @echo off
  echo [%date% %time%] Task triggered >> kalshi_log.txt
  cd /d "C:\Users\student\Downloads\BettingArbitrage-main"
  C:\Users\student\AppData\Local\Programs\Python\Python313\python.exe kalshi_scraper.py https://kalshi.com/markets/kxmasters/masters-tournament 9999
  pause
  ```
- This script is meant to be run continuously over long periods to gather time-series data.
- Change the location of the scraper and the python.exe to the folder that these files reside in your computer.

## Logic Flow
- `main()` validates CLI arguments and sets up Selenium options.
- Browser is initialized using headless Chrome via `webdriver-manager`.
- The `initatizeKalshiScrape()` loop runs the core scraping logic for a specified number of iterations.
- The scraper occasionally refreshes the page (`every 3 iterations`) to handle dynamic data updates.
- Each iteration stores new market price data into SQLite.

## Helper Functions

### `init_db(event_name)`
Initializes a database and creates a table if it does not exist.

### `scrape_polymarket()`
Core scraping function which does the following:
- Navigates or refreshes the Kalshi page.
- Clicks “More Markets” if available to load all market tiles.
- Parses Yes/No price data from each tile using button tags.
- Standardizes market names via `standardizeColumnNames()`.
- Logs prices into event-specific SQLite tables.

### `initatizeKalshiScrape()`
Manages the timed scraping loop with error handling and optional page refresh.

## Resource Management
- Uses `sqlite3` to manage local databases.
- Each market has a dedicated table in the SQLite DB.
- Browser sessions are refreshed or restarted on failure or timeouts.
- All `driver` and `conn` objects are closed properly at end of each loop or error handling block.

## Error Handling
- Graceful catching of `NoSuchElementException`, `ElementNotInteractableException`, `TimeoutError`, and general `Exception` to prevent full crashes.
- On errors like page timeout or stale browser state, a new browser session is created and the scrape resumes.

## 🪤 Pitfalls & Best Practices
### ✅ What to Do
- **Use Headless Mode:** Ideal for CI pipelines or remote/server scraping.
- **Sanitize Strings** using `standardizeColumnNames` to avoid SQL injection or malformed table names.
- **Wait for Elements** with WebDriverWait: Ensures dynamically loaded content (like Kalshi’s JS-rendered markets) is fully available before parsing.
- **Randomize Sleep Between Scrapes:** Helps avoid rate limiting or IP blocks. Use something like time.sleep(10 + random.uniform(5, 10)).

### ❌ What to Avoid
- **Too Many Iterations**: Avoid exceeding practical limits (`>9999`) to prevent browser crashes or system overloads.
- **Skipping Error Checks**: Always handle `ValueError` and `IndexError` during input parsing.
- **Using Raw Strings** for SQLite table names: always sanitize.
- **Skipping DOM Waits:** Don’t try to scrape before the page is fully loaded—Kalshi loads market data via JavaScript.
- **Over-refreshing Pages:** Avoid manually reloading frequently; Kalshi updates data automatically via JS.
- **Using Raw or Unescaped Table Names:** Never plug raw user or scraped strings directly into SQL table names—sanitize first.
- **Running Excessive Iterations (>9999):** This can lead to system slowdowns, browser crashes, or IP bans.
- **Ignoring Sleep/Delay Logic:** Constant, fast polling will likely get you blocked or throttled.
- **Skipping Error Handling:** Uncaught exceptions can kill the scraper mid-run and corrupt partial data.

---

## Usage
```bash
python kalshi_scraper.py https://kalshi.com/markets/kxmasters/masters-tournament 9999
```

## Dependencies
```bash
pip install selenium webdriver_manager
```

Ensure `standardize_names.py` is present in the working directory.

