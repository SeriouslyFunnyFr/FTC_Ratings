from flask import Flask, render_template, request, redirect, url_for
from utils.ratings import update_ratings

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

@app.route('/schedule_matches', methods=['GET', 'POST'])
def schedule_matches():
    if request.method == 'POST':
        game_number = len(matches) + 1
        blue_alliance = [request.form['blue_team1'], request.form['blue_team2']]
        red_alliance = [request.form['red_team1'], request.form['red_team2']]
        matches.append({
            'game': game_number,
            'blue_alliance': blue_alliance,
            'red_alliance': red_alliance,
            'blue_score': None,
            'red_score': None,
        })
    return render_template('schedule_matches.html', teams=teams.keys(), matches=matches)

@app.route('/record_scores', methods=['GET', 'POST'])
def record_scores():
    if request.method == 'POST':
        game_number = int(request.form['game_number'])
        blue_score = int(request.form['blue_score'])
        red_score = int(request.form['red_score'])

        # Update the match with scores
        match = matches[game_number - 1]
        match['blue_score'] = blue_score
        match['red_score'] = red_score

        # Update team ratings
        blue_team1, blue_team2 = match['blue_alliance']
        red_team1, red_team2 = match['red_alliance']
        teams[blue_team1], teams[blue_team2], teams[red_team1], teams[red_team2] = update_ratings(
            teams[blue_team1], teams[blue_team2],
            teams[red_team1], teams[red_team2],
            blue_score, red_score
        )
    return render_template('record_scores.html', matches=matches)

@app.route('/rankings')
def rankings():
    # Sort teams by rating (descending)
    sorted_teams = sorted(teams.items(), key=lambda x: x[1], reverse=True)
    return render_template('rankings.html', teams=sorted_teams)

if __name__ == '__main__':
    app.run(debug=True)
