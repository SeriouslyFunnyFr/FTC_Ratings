import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_data(url):
    response = requests.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the qualification matches table
    table = soup.find("table", {"class": "table"})

    if not table:
        return None

    # Extract headers
    headers = [th.text.strip() for th in table.find_all("th")]

    # Extract rows
    rows = []
    for tr in table.find_all("tr")[1:]:  # Skip header row
        cells = tr.find_all("td")
        row = [cell.text.strip() for cell in cells]
        rows.append(row)

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(rows, columns=headers)

    return df.to_html(classes="table table-striped")
