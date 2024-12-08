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
        EC.presence_of_element_located((By.CLASS_NAME, "Table__TBODY"))
    )

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Locate all tbody elements with the class 'Table__TBODY'
    tbody_tables = soup.find_all('tbody', class_='Table__TBODY')
    
    # Initialize a list to store all table data
    all_data = []

    for tbody in tbody_tables:
        rows = tbody.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if cells:  # Process rows with actual data
                # Convert all cell text into strings to avoid misinterpretation
                all_data.append([str(cell.text.strip()) for cell in cells])

    # Dynamically generate column names based on the maximum number of columns
    max_columns = max(len(row) for row in all_data) if all_data else 0
    headers = [f"Column {i+1}" for i in range(max_columns)]

    # Create DataFrame if data is available
    if all_data:
        df = pd.DataFrame(all_data, columns=headers)

        # Explicitly format all columns as strings in the DataFrame
        df = df.astype(str)

        # Specify the file path where the CSV will be saved
        file_path = os.path.join(os.getcwd(), 'nba_team_tbody_data_testing.csv')

        # Save DataFrame to CSV
        df.to_csv(file_path, index=False, quoting=1)  # quoting=1 ensures all fields are quoted

        print(f"Data successfully saved to {file_path}")
    else:
        print("No data found in 'Table__TBODY'.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
