# BettingArbitrage
## Project Introduction:
ZipAdvisors is developing an arbitrage monitoring software for prediction markets, focusing on identifying price discrepancies between Kalshi and Polymarket. The project consists of a backend data pipeline that collects data via a custom-built web scraper. We coded it with the selenium and requests library. The scrapper processes, and stores market data, coupled with analytical tools to detect trading opportunities. We chose a scrapper instead of an API to collect our data because an API call wouldn’t be as frequent as a real-time web scraper.
By systematically tracking yes/no contract prices across these platforms, the software aims to uncover mispricings that could yield risk-free profits through carefully balanced positions. This tool is designed for hobbyists who sports bet, providing them with real-time insights and historical trends to inform their betting strategies.
## Overall Goal:
The primary objective is to create a reliable, automated software that continuously monitors prediction markets for arbitrage opportunities with the end goal of creating an unfair information advantage for clients of our product. Much like the data products that power hedge funds, CIA, and military units, we wanted to bring that same informational edge to your hobbyist sports-better.
We do so by programming our product to collect pricing data, identify statistically significant divergences between equivalent contracts, and generate actionable advice for traders. Beyond immediate arbitrage detection, the software also maintains a historical database to support volatility analysis, backtesting, and strategy development. Ultimately, the goal is to offer users a competitive edge by highlighting inefficiencies in these rapidly evolving markets.
## Data Pipeline:
The current implementation consists of dual-engine Python-based web scrapers—one for Kalshi, and another for Polymarket—both built using Selenium to handle dynamic content. These scrapers run on scheduled intervals via batch scripts, capturing market names, yes/no prices, and trading volumes. The data is standardized to ensure consistency and stored in SQLite databases, with each market maintaining its own table. A helper function sanitizes market names to prevent SQL injection and ensure compatibility with database naming conventions. We run the dual-engine scrapers on a VM (Virtual Machine) on NYU’s servers.
Looking ahead, we plan to build a User Interface for the software, served on a web-server. The frontend architecture will be composed of HTML, CSS, and JavaScript, wrapped in the Python web framework, Flask.
Aside from the obvious buttons we want to create to allow the sports-betting-client to interact with real-time market data, we want to make a financial dashboard where the client will feel like he has information at his fingertips. Something along the lines of, and inspired by, Bloomberg Terminals, S&P CapIQ, or Palantir Technologies– in the respect that users feel like they are at an incredible information advantage when using our product.

USAGE: 
Make sure to import relevant dependencies (Selenium, Chrome Driver, WebDriver Manager, requests) and append them to the path you are using the system on

On your system terminal, type python then either script name and then you are REQUIRED to specify two arguments in order: the link you are scraping, and the # of iterations you will scrape. The scraper scrapes every 20-25 seconds, so a full day's worth of scraping is at max 4320 iterations. 

Example usage on a Linux/MacOS bash terminal:
python kalshi_scraper.py https:/mykalshiurl.com/event 4320 & polymarket_scraper.py https:/mypolymarket.com/event 4320

On Windows CMD:
start python kalshi_scraper.py https:/mykalshiurl.com/event 4320 & start python polymarket_scraper.py https:/mypolymarket.com/event 4320


