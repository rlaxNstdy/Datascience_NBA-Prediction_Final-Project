from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
url = "https://www.nba.com/stats/teams/traditional"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Function to extract data from the current page
def scrape_page(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'Crom_table__p1iZz'})
    if not table:
        print("Table not found.")
        return None, None
    
    # Extract headers (only needed once)
    headers = [th.getText() for th in table.find('thead').find_all('th')]
    
    # Extract rows of data
    rows = table.find('tbody').find_all('tr')
    data = [[td.getText() for td in row.find_all('td')] for row in rows]
    
    return headers, data

# Initialize data storage
all_data = []
headers = None

# Pagination handling
while True:
    # Scrape current page
    page_headers, page_data = scrape_page(driver)
    if page_data:
        all_data.extend(page_data)
        if headers is None:
            headers = page_headers  # Set headers on the first page
    
    # Check if "Next" button is disabled
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.stats-table-pagination__next'))
        )
        if "disabled" in next_button.get_attribute("class"):
            print("Reached the last page.")
            break
        # Click the "Next" button
        ActionChains(driver).move_to_element(next_button).click(next_button).perform()
        time.sleep(5)  # Wait for the page to load
    except Exception as e:
        print(f"Pagination error or no next button: {e}")
        break

# Create a DataFrame
if headers and all_data:
    df = pd.DataFrame(all_data, columns=headers)
    df.to_csv("nba_team_stats_regularseason.csv", index=False)
    print("Data saved to nba_team_stats_regularseason.csv")
else:
    print("No data scraped.")

# Close the browser
driver.quit()
