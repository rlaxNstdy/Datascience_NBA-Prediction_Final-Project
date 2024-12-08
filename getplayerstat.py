from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import os

# Set up the Selenium WebDriver
driver = webdriver.Chrome()  # Assumes chromedriver is in PATH

url = "https://www.espn.com/nba/standings/_/season/2022/group/league"
driver.get(url)

try:
    # Wait for the main table container to load
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CLASS_NAME, "Table__ScrollerWrapper"))
    )

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Locate the table container
    table_wrapper = soup.find('div', class_='Table__ScrollerWrapper relative overflow-hidden')
    if not table_wrapper:
        print("Table wrapper not found. The content might be dynamically loaded.")
    else:
        # Extract headers
        header_container = table_wrapper.find('thead')
        headers = [header.text.strip() for header in header_container.find_all('th')]

        # Extract rows
        body_container = table_wrapper.find('tbody')
        rows = body_container.find_all('tr') if body_container else []
        data = []
        for row in rows:
            cells = row.find_all('td')
            if cells:  # Process rows with actual data
                data.append([cell.text.strip() for cell in cells])

        # Create DataFrame if headers and data are available
        if headers and data:
            df = pd.DataFrame(data, columns=headers)

            # Specify the file path where the CSV will be saved
            file_path = os.path.join(os.getcwd(), 'nba_team_standing_2021-22.csv')

            # Save DataFrame to CSV
            df.to_csv(file_path, index=False)
            print(f"Data successfully saved to {file_path}")
        else:
            print("No headers or data found in the table.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
