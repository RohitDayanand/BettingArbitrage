#Make sure to download relevant dependencies: selenium, webdriver_manager, sqlite3
#This script scrapes the Kalshi website for the latest prices of the markets and stores them in a database
import os
import time
import sys
import sqlite3
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from standardize_names import standardizeColumnNames

# Checker to avoid duplicate and invalid table creation/queries
def standardizeColumnNames(s):
    s = s.lower().replace(" ", "_")
    s = s.replace("?", "")
    s = s.replace(":", "")
    s = s.replace("(", "")
    s = s.replace(")", "")
    s = s.replace("/", "")
    s = s.replace("-", "_")
    s = s.replace(",", "")
    s = s.replace(".", "")
    s = s.replace("°", "")
    s = s.replace("’", "")
    s = s.replace("‘", "")
    s = s.replace("”", "")
    s = s.replace(">", "plus_")
    s = s.replace("<", "minus_")
    s = s.replace("=", "equals_")
    if s[0].isdigit():
        s = "num_" + s
    return s

def init_db(event_name):
    conn = sqlite3.connect("scraper_demo1.db")
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {event_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            market_name TEXT,
            trading_volume TEXT,
            yes_price REAL,
            no_price REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    return 0

# Function to scrape data

def scrape_polymarket(url, event_id, table_created, driver):
    try:
        driver.get(url)
    except Exception as e:
        print("Error loading page", e)
        return
    time.sleep(6)  # Allow time for page to load
    # Click the "More Markets" button if it exists
    button_elements = driver.find_elements(By.XPATH, "//div[@style='flex: 1 1 0%;']")
    try:
        more_market_button = button_elements[-1]
        print(more_market_button.text)
        first_clickable = more_market_button.find_element(By.XPATH, ".//*[self::button or self::a or self::span or @role='button' or @onclick]")
        first_clickable.click()
        time.sleep(2)
    except NoSuchElementException as e:
        print("No more markets button")
    except ElementNotInteractableException as e:
        print("More markets button not interactable")
    except Exception as e: 
        print("Other error", e)

    # Find all market tiles for the event
    markets_containers = driver.find_elements(By.XPATH, "//div[starts-with(@class, 'binaryMarketTile-0-1-')]")

    print(f"Found {len(markets_containers)} markets") # Print the number of markets found
    
    for market in markets_containers:
        market_name = market.find_element(By.XPATH, ".//span[contains(@class, 'lining-nums') and contains(@class, 'tabular-nums')]/div")
        
        #java-script to get the inner text of the element - some information is not directly accessible
        market_name_text = standardizeColumnNames(driver.execute_script("return arguments[0].innerText;", market_name))
    
        buttons = market.find_elements(By.TAG_NAME, "button")

        yes_price = 0.0
        no_price = 0.0

        for button in buttons:
            if "Yes" in button.text:
                try:
                    yes_price = float(button.text.split()[-1].replace('¢', '')) / 100
                except ValueError:
                    print("Error converting yes price to float, will put as 0", button.text.split()[-1].replace('¢', ''))
                    yes_price = 0
            elif "No" in button.text:
                try:
                    no_price = float(button.text.split()[-1].replace('¢', '')) / 100
                except ValueError:
                    print("Error converting yes price to float, will put as 0", button.text.split()[-1].replace('¢', ''))
                    no_price = 0

        print(f"Event: {market_name_text} | Yes: {yes_price} | No: {no_price}")
        # Close the driver and database connection

        conn = sqlite3.connect(f"{event_id}_kalshi.db")
        cursor = conn.cursor()

        # Save to database
        if not table_created:
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {market_name_text} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market_name TEXT,
                yes_price REAL,
                no_price REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                ''')
            conn.commit()
        cursor.execute(f"""
            INSERT INTO {market_name_text} (market_name, yes_price, no_price) VALUES (?, ?, ?)""",
            (market_name_text, yes_price, no_price))
        conn.commit()
    conn.commit()
    conn.close()
    print("Scraping completed")  # Close connection
    

def initatizeKalshiScrape(event_id, event_url, iterations, driver):
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
    initatizeKalshiScrape(event_id, event_url, iterations, driver)

if __name__ == "__main__":
    main()
