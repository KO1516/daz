
import pandas as pd
import requests
import time

# Load your original dataset
df = pd.read_csv("games_dataset.csv")

# Ensure the game name column exists
if "Game Name" not in df.columns:
    raise ValueError("Expected a column named 'Game Name' in the dataset.")

# Sample known mappings for demonstration (can be expanded or automated)
known_steam_ids = {
    "Dota 2": 570,
    "Portal 2": 620,
    "Counter-Strike: Global Offensive": 730,
    "Team Fortress 2": 440,
    "Left 4 Dead 2": 550,
    "Half-Life 2": 220
}

# Function to query Steam API
def fetch_steam_data(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json().get(str(appid), {}).get("data", {})
            if data:
                return {
                    "Steam AppID": appid,
                    "Steam Title": data.get("name"),
                    "Release Date": data.get("release_date", {}).get("date"),
                    "Metacritic Score": data.get("metacritic", {}).get("score"),
                    "Price (USD)": data.get("price_overview", {}).get("final", 0) / 100 if data.get("price_overview") else "Free",
                    "Platforms": ", ".join([k for k, v in data.get("platforms", {}).items() if v])
                }
    except Exception as e:
        print(f"Error for AppID {appid}: {e}")
    return {}

# Create enrichment list
enriched_data = []

# Loop through known matches and fetch data
for title, appid in known_steam_ids.items():
    game_data = fetch_steam_data(appid)
    if game_data:
        game_data["Game Name"] = title
        enriched_data.append(game_data)
    time.sleep(1)  # avoid hitting Steam rate limits

# Convert to DataFrame
steam_df = pd.DataFrame(enriched_data)

# Merge with original dataset
merged_df = df.merge(steam_df, on="Game Name", how="left")

# Save result
merged_df.to_csv("games_dataset_enriched_with_steam.csv", index=False)
print("✅ Enriched dataset saved as 'games_dataset_enriched_with_steam.csv'")
