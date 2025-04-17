
# Backend High Level

For our backend, we have two main Python scripts responsible for scraping data from prediction markets:
- `polymarket_scraper.py`
- `kalshi_scraper.py`

These scripts use **Selenium** to automate browser actions and extract market data from the given URLs on **Polymarket** and **Kalshi**, respectively.

## What We Scrape

For each prediction market page, we scrape:
- Market names (standardized for database entry)
- "Yes" and "No" prices (converted to floats)
- Trading volume (when available)
- Timestamps for when the data was retrieved

The extracted data is stored in a **SQLite** database, with one table per market.

## Automation via Batch Files

We use the following batch files to continuously run the scrapers in an automated loop:
- `polymarket_scraper_scheduler.bat`
- `kalshi_scraper_scheduler.bat`

These batch files:
- Launch the Python script with required arguments (URL and number of iterations)
- Continuously execute the scraper in a timed loop
- Allow recovery and restarts on failure (via script logic)
- Write data to a local SQLite database for further use

## Execution Context

Each scraper is invoked with parameters:
- `event_url`: the market URL to scrape
- `iterations`: how many times to scrape the data in a loop

These parameters are passed from the batch file. For example, `kalshi_scraper_scheduler.bat` runs the scraper with:

```
C:\Users\student\AppData\Local\Programs\Python\Python313\python.exe kalshi_scraper.py https://kalshi.com/markets/kxmasters/masters-tournament 9999
```

## Summary

This backend setup allows for reliable, headless scraping of live market data from prediction platforms, storing it into local databases for further analysis or dashboard display.
