import requests
import time
import trueskill as ts

# API Credentials (Replace with your actual credentials)
USERNAME = "your_username"
ACCESS_TOKEN = "your_access_token"
BASE_URL = "https://ftc-events.firstinspires.org/v2.0"

# Headers for authentication
HEADERS = {
    "Authorization": f"Basic {USERNAME}:{ACCESS_TOKEN}",
    "Accept": "application/json"
}

# Initialize TrueSkill environment
env = ts.TrueSkill()
teams = {}  # Dictionary to store team ratings

def get_event_matches(event_code, season=2023):
    """Fetches match results for a given event."""
    url = f"{BASE_URL}/{season}/matches/{event_code}"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching match data: {response.status_code}")
        return None

def update_ratings(red_team, blue_team, red_score, blue_score):
    """Updates ratings using TrueSkill."""
    for team in red_team + blue_team:
        if team not in teams:
            teams[team] = env.create_rating()
    
    if red_score > blue_score:
        new_ratings = env.rate([(teams[red_team[0]], teams[red_team[1]]), (teams[blue_team[0]], teams[blue_team[1]])])
    else:
        new_ratings = env.rate([(teams[blue_team[0]], teams[blue_team[1]]), (teams[red_team[0]], teams[red_team[1]])])
    
    teams[red_team[0]], teams[red_team[1]] = new_ratings[0]
    teams[blue_team[0]], teams[blue_team[1]] = new_ratings[1]

def update_live_scores(event_code, interval=30):
    """Continuously fetches and updates match data every `interval` seconds."""
    while True:
        matches = get_event_matches(event_code)
        if matches:
            print("Updated Match Data:")
            for match in matches.get("matches", []):
                red_team = match["red"]
                blue_team = match["blue"]
                red_score = match["redScore"]
                blue_score = match["blueScore"]
                update_ratings(red_team, blue_team, red_score, blue_score)
                print(f"Match {match['matchNumber']}: {red_score} - {blue_score}")
        time.sleep(interval)  # Wait before fetching again

if __name__ == "__main__":
    EVENT_CODE = "YourEventCodeHere"  # Replace with actual event code
    update_live_scores(EVENT_CODE)
