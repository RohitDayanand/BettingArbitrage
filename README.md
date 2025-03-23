# BettingArbitrage
Tools for scraping, storing, and visualizing peer bets in Polymarket and Kalshi to identify arbitrage opportunities

USAGE: 
Make sure to import relevant dependencies (Selenium, Chrome Driver, WebDriver Manager, requests) and append them to the path you are using the system on

On your system terminal, type python then either script name and then you are REQUIRED to specify two arguments in order: the link you are scraping, and the # of iterations you will scrape. The scraper scrapes every 20-25 seconds, so a full day's worth of scraping is at max 4320 iterations. 

Example usage on a Linux/MacOS bash terminal:
python kalshi_scraper.py https:/mykalshiurl.com/event 4320 & polymarket_scraper.py https:/mypolymarket.com/event 4320

On Windows CMD:
start python kalshi_scraper.py https:/mykalshiurl.com/event 4320 & start python polymarket_scraper.py https:/mypolymarket.com/event 4320


