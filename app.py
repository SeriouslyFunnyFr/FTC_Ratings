from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from trueskill import Rating, rate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ftc_ratings.db'
db = SQLAlchemy(app)

# Database Models
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    rating_mu = db.Column(db.Float, default=25.0)
    rating_sigma = db.Column(db.Float, default=8.333)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blue_alliance = db.Column(db.String(100), nullable=False)
    red_alliance = db.Column(db.String(100), nullable=False)
    blue_score = db.Column(db.Integer, nullable=False)
    red_score = db.Column(db.Integer, nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teams')
def teams():
    teams = Team.query.order_by(Team.rating_mu.desc()).all()
    return render_template('teams.html', teams=teams)

@app.route('/matches')
def matches():
    matches = Match.query.all()
    return render_template('matches.html', matches=matches)

@app.route('/link_api', methods=['GET', 'POST'])
def link_api_view():
    if request.method == 'POST':
        team_number = request.form['team_number']
        event_code = request.form['event_code']
        # Fetch team data from the API
        response = requests.get(f'http://api.example.com/teams/{team_number}/events/{event_code}')
        if response.status_code == 200:
            team_data = response.json()
            team_name = team_data.get('name', 'Unknown Team')
            # Process the data for TrueSkill (replace this with logic)
            result = f"Data for team {team_name} at event {event_code}"
            return f'<h1>Result: {result}</h1>'
        else:
            return '<h1>Error fetching team data</h1>'
    return render_template('link_api.html')

        # Add match to database
        new_match = Match(blue_alliance=blue_alliance, red_alliance=red_alliance, blue_score=blue_score, red_score=red_score)
        db.session.add(new_match)
        db.session.commit()
        return redirect(url_for('matches'))
    teams = Team.query.all()
    return render_template('add_match.html', teams=teams)

def update_ratings(blue_alliance, red_alliance, blue_score, red_score):
    blue_teams = [Team.query.filter_by(name=name.strip()).first() for name in blue_alliance.split(',')]
    red_teams = [Team.query.filter_by(name=name.strip()).first() for name in red_alliance.split(',')]

    # Convert to TrueSkill ratings
    blue_ratings = [Rating(mu=team.rating_mu, sigma=team.rating_sigma) for team in blue_teams]
    red_ratings = [Rating(mu=team.rating_mu, sigma=team.rating_sigma) for team in red_teams]

    # Update ratings based on match outcome
    if blue_score > red_score:
        new_blue_ratings, new_red_ratings = rate([blue_ratings, red_ratings], ranks=[0, 1])
    else:
        new_blue_ratings, new_red_ratings = rate([blue_ratings, red_ratings], ranks=[1, 0])

    # Save updated ratings
    for i, team in enumerate(blue_teams):
        team.rating_mu = new_blue_ratings[i].mu
        team.rating_sigma = new_blue_ratings[i].sigma
    for i, team in enumerate(red_teams):
        team.rating_mu = new_red_ratings[i].mu
        team.rating_sigma = new_red_ratings[i].sigma
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
