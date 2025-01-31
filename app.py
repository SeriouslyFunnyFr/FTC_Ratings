from flask import Flask, render_template, request, redirect, url_for
from utils.ratings import update_ratings
from utils.scraper import scrape_matches  # Import the scraper function

app = Flask(__name__)

# In-memory storage for teams, matches, and ratings
teams = {}  # Format: {'Team A': 1000, 'Team B': 1000, ...}
matches = []  # Format: [{'game': 1, 'blue_alliance': ['Team A', 'Team B'], 'red_alliance': ['Team C', 'Team D'], 'blue_score': None, 'red_score': None}, ...]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_teams', methods=['GET', 'POST'])
def add_teams():
    if request.method == 'POST':
        team_name = request.form['team_name']
        if team_name and team_name not in teams:
            teams[team_name] = 1000  # Default rating for new teams
    return render_template('add_teams.html', teams=teams.keys())

@app.route('/scrape_matches', methods=['GET', 'POST'])
def scrape_matches_route():
    if request.method == 'POST':
        url = request.form['url']
        try:
            scraped_matches = scrape_matches(url)  # Scrape matches from the provided URL
            for match in scraped_matches:
                # Add teams if they don't exist
                for team in match['blue_alliance'] + match['red_alliance']:
                    if team not in teams:
                        teams[team] = 1000
                # Add the match to the matches list
                matches.append(match)
            return redirect(url_for('rankings'))
        except Exception as e:
            return f"Error scraping matches: {str(e)}"
    return render_template('scrape_matches.html')

@app.route('/rankings')
def rankings():
    # Sort teams by rating (descending)
    sorted_teams = sorted(teams.items(), key=lambda x: x[1], reverse=True)
    return render_template('rankings.html', teams=sorted_teams)

if __name__ == '__main__':
    app.run(debug=True)
