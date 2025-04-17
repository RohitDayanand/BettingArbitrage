
# High-Level Module Overview

## Core Modules

### 1. **Scraper Modules**
These scripts use Selenium to scrape prediction market data from Polymarket and Kalshi.

#### `polymarket_scraper.py`
- **Purpose:** Scrapes event and market data from Polymarket URLs.
- **Key Functions:**
  - `scrape_polymarket`: Navigates to event URL and extracts market names, yes/no prices, volume, and timestamps.
  - `polymarket_scraper`: Coordinates scraping in a loop for a set number of iterations, handles exceptions.
  - `main`: Parses command-line arguments and initiates the scraping session.
- **Notable Modules Used:**
  - `selenium`
  - `sqlite3`
  - `webdriver_manager`
  - `datetime`
  - `standardize_names`

#### `kalshi_scraper.py`
- **Purpose:** Scrapes market data from Kalshi using event URLs.
- **Key Functions:**
  - `scrape_polymarket`: (Despite the reused name) Extracts market names and yes/no prices, optionally clicking "More Markets".
  - `initatizeKalshiScrape`: Manages scraping loop and refresh cycles.
  - `main`: Handles input arguments and sets up the headless browser.
- **Notable Modules Used:**
  - `selenium`
  - `sqlite3`
  - `webdriver_manager`
  - `datetime`
  - `standardize_names`

#### Python Modules Used:

- `time`→ Manages delays and iteration pacing between scraper cycles.
- `sqlite3`→ Manages SQLite database connections and data persistence; Writes market data to a local database.
- `random`→ Adds randomness to sleep intervals to simulate natural scraping behavior.
- `webdriver_manager.chrome`→ Automatically handles the downloading and management of the Chrome WebDriver binary; Manages driver installations.
- `standardize_names`→ Contains a custom utility function standardizeColumnNames() to normalize market names for consistent database schema.
- `urllib3.exceptions.ReadTimeoutError`→ Handles timeout exceptions when a web page fails to load.
- `datetime`→ Records timestamps for scraped data entries.
- `os` (only in kalshi_scraper)→ Used for general system-level operations (optional usage in Kalshi context).
- `sys`→ Parses command-line arguments for URLs and iteration counts passed to the script.
- `selenium` (and submodules)→ Automates browser interactions for scraping web content. Used extensively for DOM interaction, navigation, and dynamic content loading.

### 2. **Standardization Module**

#### `standardize_names.py`
- **Purpose:** Provides functions to clean and format market names and table names consistently for database compatibility.
- **Key Functions:**
  - `standardizeColumnNames`: Converts raw strings to standardized format (e.g., removes special characters, replaces spaces).

### 3. **Scheduler Batch Files**
- **Purpose:** These files are used to schedule and run the scraping scripts automatically.

#### `polymarket_scraper_scheduler`
- **Primary Function:** Calls `polymarket_scraper.py` with appropriate arguments at scheduled intervals.

#### `kalshi_scraper_scheduler`
- **Primary Function:** Automates execution of `kalshi_scraper.py`, typically via cron job or task scheduler.

### 4. **Database Analysis and Hypothesis Testing**

#### `PolymarketPredicter.ipynb`
- **Primary Function:** Analyze both datasets to train ML models to predict the movement of Polymarket prices using Kalshi prices. 

---

## Summary of Data Flow
1. **Input:** Event URL and iteration count.
2. **Process:**
   - Open headless Chrome browser with Selenium.
   - Extract relevant market data (names, prices, volume).
   - Standardize data.
3. **Output:**
   - Store results in SQLite database (table per market).
4. **Analyze:**
   - Examine the data from the Polymarket and Kalshi datasets to train ML models to predict Polymarket using Kalshi.
