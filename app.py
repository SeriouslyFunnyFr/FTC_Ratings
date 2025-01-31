from flask import Flask, render_template, request, redirect, url_for
from utils.ratings import update_ratings

app = Flask(__name__)

# In-memory storage for teams and their ratings
teams = {}  # Format: {'Team A': 1000, 'Team B': 1000, ...}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/record_match', methods=['GET', 'POST'])
def record_match():
    if request.method == 'POST':
        # Get team names and scores
        alliance1_team1 = request.form['alliance1_team1']
        alliance1_team2 = request.form['alliance1_team2']
        alliance2_team1 = request.form['alliance2_team1']
        alliance2_team2 = request.form['alliance2_team2']
        alliance1_score = int(request.form['alliance1_score'])
        alliance2_score = int(request.form['alliance2_score'])

        # Add new teams if they don't exist
        for team in [alliance1_team1, alliance1_team2, alliance2_team1, alliance2_team2]:
            if team not in teams:
                teams[team] = 1000  # Default rating for new teams

        # Update ratings using TrueSkill
        teams[alliance1_team1], teams[alliance1_team2], teams[alliance2_team1], teams[alliance2_team2] = update_ratings(
            teams[alliance1_team1], teams[alliance1_team2],
            teams[alliance2_team1], teams[alliance2_team2],
            alliance1_score, alliance2_score
        )
        return redirect(url_for('rankings'))

    return render_template('record_match.html', teams=teams.keys())

@app.route('/rankings')
def rankings():
    # Sort teams by rating (descending)
    sorted_teams = sorted(teams.items(), key=lambda x: x[1], reverse=True)
    return render_template('rankings.html', teams=sorted_teams)

if __name__ == '__main__':
    app.run(debug=True)
