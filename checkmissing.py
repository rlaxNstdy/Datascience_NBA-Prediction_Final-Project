import pandas as pd

# Load your merged dataset
# merged_df = pd.read_csv("all_nba_player_draft_2021-2024.csv")
# merged_df = pd.read_csv("all_nba_player_stats 2021-2024_regular.csv")
# merged_df = pd.read_csv("all_nba_player_stats_pre.csv")
merged_df = pd.read_csv("all_nba_team_stats_combined.csv")

# Check for missing values
missing_values = merged_df.isnull().sum()

# Print columns with missing values
print("Missing values per column:")
print(missing_values)

# Check if there are any missing values in the entire dataset
if missing_values.sum() > 0:
    print("\nThere are missing values in the dataset.")
else:
    print("\nThere are no missing values in the dataset.")
