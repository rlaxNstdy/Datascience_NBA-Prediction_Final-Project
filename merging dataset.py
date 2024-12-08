import pandas as pd

# File paths with corresponding seasons
file_paths = [
    ("nba_team_standing_2021-22.csv", "2021-21"),
    ("nba_team_standing_2022-23.csv", "2022-23"),
    ("nba_team_standing_2023-24.csv", "2023-24"),
    ("nba_team_standing_2024-24.csv", "2023-24"),
    
]

# Combine the data
dataframes = []
for file_path, season in file_paths:
    df = pd.read_csv(file_path)
    df['Season'] = season  # Add season column
    dataframes.append(df)

# Concatenate all dataframes
merged_df = pd.concat(dataframes, ignore_index=True)

# Save the merged dataframe to a new file
merged_df.to_csv("all_nba_standing_2021-2025.csv", index=False)

print("Merged dataset created and saved as 'nba_team_stats_combined.csv'.")
