# BettingArbitrage
## Project Introduction:
ZipAdvisors is developing an arbitrage monitoring software for prediction markets, focusing on identifying price discrepancies between Kalshi and Polymarket. The project consists of a backend data pipeline that collects data via a custom-built web scraper. We coded it with the selenium and requests library. The scrapper processes, and stores market data, coupled with analytical tools to detect trading opportunities. We chose a scrapper instead of an API to collect our data because an API call wouldn’t be as frequent as a real-time web scraper.
By systematically tracking yes/no contract prices across these platforms, the software aims to uncover mispricings that could yield risk-free profits through carefully balanced positions. This tool is designed for hobbyists who sports bet, providing them with real-time insights and historical trends to inform their betting strategies.
## Overall Goal:
The primary objective is to create a reliable, automated software that continuously monitors prediction markets for arbitrage opportunities for clients of our product. Much like the data products that power hedge funds, CIA, and military units, we wanted to bring that same informational edge to your hobbyist sports-better.
We do so by programming our product to collect pricing data, identify statistically significant divergences between equivalent contracts, and generate actionable advice for traders. Beyond immediate arbitrage detection, the software also maintains a historical database to support volatility analysis, backtesting, and strategy development. Ultimately, the goal is to offer users a competitive edge by highlighting inefficiencies in these rapidly evolving markets.

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


USAGE: 
Make sure to import relevant dependencies (Selenium, Chrome Driver, WebDriver Manager, requests) and append them to the path you are using the system on

On your system terminal, type python then either script name and then you are REQUIRED to specify two arguments in order: the link you are scraping, and the # of iterations you will scrape. The scraper scrapes every 20-25 seconds, so a full day's worth of scraping is at max 4320 iterations. 

Example usage on a Linux/MacOS bash terminal:
python kalshi_scraper.py https:/mykalshiurl.com/event 4320 & polymarket_scraper.py https:/mypolymarket.com/event 4320

On Windows CMD:
start python kalshi_scraper.py https:/mykalshiurl.com/event 4320 & start python polymarket_scraper.py https:/mypolymarket.com/event 4320


