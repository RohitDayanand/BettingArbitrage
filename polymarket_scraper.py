import time
import sqlite3
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from standardize_names import standardizeColumnNames

import sys

# Function to scrape data
def scrape_polymarket(url, event_id, table_created, driver):
    try:
        driver.get(url)
    except Exception as e:
        print("Error loading page", e)
        return
    time.sleep(6)  # Allow time for page to load

    # Extract event name and standardize it
    table_name = standardizeColumnNames(event_id)
    
    print(table_name)
    
    # Locate the container div for all markets
    markets_containers = driver.find_elements(By.XPATH, "//div[contains(@class, 'c-iuGBSs')]")
    print(f"Found {len(markets_containers)} markets")
    
    for market in markets_containers:
        market_name = standardizeColumnNames(market.find_element(By.XPATH, ".//p[contains(@class, 'c-cZBbTr')]").text)
        yes_price = market.find_element(By.XPATH, ".//div[contains(text(), 'Buy Yes')]").text.split()[-1].replace('¢', '')
        no_price = market.find_element(By.XPATH, ".//div[contains(text(), 'Buy No')]").text.split()[-1].replace('¢', '')
        this_trading_volume = market.find_element(By.XPATH, ".//p[contains(., 'Vol.')]").text
       
        this_trading_volume = this_trading_volume.split()[0].replace('$', '').replace(',', '')

        try:
            this_trading_volume = float(this_trading_volume)

        except ValueError:
            print("Error converting trading volume to float, will have strings",   this_trading_volume)
            
        print(this_trading_volume)
        
        print(market_name)
        # Convert to float
        yes_price = float(yes_price) / 100
        no_price = float(no_price) / 100
        
        #Format market name for SQlite tabular entry
        print(f"Event: {market_name} | Volume: {this_trading_volume} | Yes: {yes_price} | No: {no_price}")
        
        # Connect to SQLite database
        conn = sqlite3.connect(f"{table_name}_polymarket.db")
        cursor = conn.cursor()
        cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {market_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market_name TEXT,
                trading_volume TEXT,
                yes_price REAL,
                no_price REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
        ''')
        conn.commit()
        cursor.execute(f"""
            INSERT INTO {market_name} (market_name, trading_volume, yes_price, no_price) VALUES (?, ?, ?, ?)""",
            (market_name, this_trading_volume, yes_price, no_price))
        conn.commit()
    conn.commit()
    conn.close()
    print("Scraping completed")  # Close connection
    
def polymarket_scraper(event_url, event_id, iterations, driver):
    print("The number of recorded iterations are", iterations)
    table_created = False
    counter = 0
    while counter < iterations:
        scrape_polymarket(event_url, event_id, table_created, driver)  # Replace with actual event name
        counter += 1
        driver.refresh()
        time.sleep(10 + int(random.uniform(5,10)))  # Run every minute

    driver.quit()

def main():
    if len(sys.argv) < 3:
        print("Please provide an event url and a number of iterations (this scraper refreshes every ~30 seconds)" )
        return
    else:
        event_url = ""
        iterations = 0
        try:
            event_url = sys.argv[1]
            iterations = int(sys.argv[2])
            event_id = event_url.split("/")[-1]
        except ValueError:
            print("Please provide a valid event ID")
        except IndexError:
            print("Please provide a valid number of iterations")
        except Exception as e:  
            print("Error", e)
        if not event_url:
            print("Please provide a valid event ID")
            return
        if not iterations:
            print("Please provide a valid number of iterations")
        if iterations <= 0 or iterations > 1000:
            print("Please provide a valid number of iterations, or not too many")
            return
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # Add this line to make the browser headless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    polymarket_scraper(event_url, event_id, iterations, driver)

if __name__ == "__main__":
    main()