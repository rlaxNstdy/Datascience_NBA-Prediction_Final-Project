from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and in PATH
url = "https://www.espn.com/nba/standings/_/group/leaguettps://www.basketball-reference.com/leagues/NBA_2021.html"
driver.get(url)

# Wait for the page to load (adjust this if the page is slow)
time.sleep(5)

# Parse the page source with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Locate the table by its ID
table = soup.find('table', {'id': 'per_game-team'})

# Check if the table exists
if not table:
    print("Table with ID 'per_game-team' not found on the page.")
else:
    # Extract headers for the 'per_game-team' table
    headers = [th.getText() for th in table.find('thead').find_all('th')][1:]  # Skip the first empty header

    # Extract rows of data from the 'per_game-team' table
    rows = table.find('tbody').find_all('tr')
    data = []
    for row in rows:
        if row.find('td'):  # Check for data rows
            data.append([td.getText() for td in row.find_all('td')])

    # Create a DataFrame for 'per_game-team'
    df_per_game = pd.DataFrame(data, columns=headers)
    print("Extracted data from 'per_game-team'.")

# Locate the 'Table__TBODY' element
tbody_tables = soup.find_all('tbody', class_='Table__TBODY')
all_data = []  # To store data from all tbody tables

# Iterate over each tbody table found
for tbody in tbody_tables:
    rows = tbody.find_all('tr')
    for row in rows:
        if row.find('td'):  # Check for data rows
            all_data.append([td.getText() for td in row.find_all('td')])

# Create a DataFrame for 'Table__TBODY'
if all_data:
    # Using generic column names since headers may vary
    max_columns = max(len(row) for row in all_data)  # Find the maximum number of columns in rows
    headers_tbody = [f"Column {i+1}" for i in range(max_columns)]
    df_tbody = pd.DataFrame(all_data, columns=headers_tbody)
    print("Extracted data from 'Table__TBODY'.")
else:
    print("No data found in 'Table__TBODY'.")

# Save the data to CSV files
if 'df_per_game' in locals():
    df_per_game.to_csv("nba_team_stats_per_game.csv", index=False)
    print("Data saved to 'nba_team_stats_per_game.csv'.")

if all_data:
    df_tbody.to_csv("nba_team_standing.csv", index=False)
    print("Data saved to 'nba_team_stat.csv'.")

# Close the browser
driver.quit()