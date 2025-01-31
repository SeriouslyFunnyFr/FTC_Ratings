import requests
from bs4 import BeautifulSoup

def scrape_matches(url):
    # Send a GET request to the website
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table containing match data
    table = soup.find('table', {'class': 'match-table'})
    if not table:
        raise Exception("Match table not found on the page.")

    # Extract match data
    matches = []
    rows = table.find_all('tr')[1:]  # Skip the header row
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 7:  # Ensure the row has enough columns
            match = {
                'game': int(columns[0].text.strip()),  # Match number
                'blue_alliance': [columns[1].text.strip(), columns[2].text.strip()],  # Blue alliance teams
                'red_alliance': [columns[3].text.strip(), columns[4].text.strip()],  # Red alliance teams
                'blue_score': int(columns[5].text.strip()),  # Blue alliance score
                'red_score': int(columns[6].text.strip()),  # Red alliance score
            }
            matches.append(match)

    return matches
