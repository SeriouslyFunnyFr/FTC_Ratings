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

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        new_team = Team(name=name)
        db.session.add(new_team)
        db.session.commit()
        return redirect(url_for('teams'))
    return render_template('add_team.html')

@app.route('/add_match', methods=['GET', 'POST'])
def add_match():
    if request.method == 'POST':
        blue_alliance = f"{request.form['blue_team1']}, {request.form['blue_team2']}"
        red_alliance = f"{request.form['red_team1']}, {request.form['red_team2']}"
        blue_score = int(request.form['blue_score'])
        red_score = int(request.form['red_score'])

        # Update ratings
        update_ratings(blue_alliance, red_alliance, blue_score, red_score)

        # Add match to database
        new_match = Match(blue_alliance=blue_alliance, red_alliance=red_alliance, blue_score=blue_score, red_score=red_score)
        db.session.add(new_match)
        db.session.commit()
        return redirect(url_for('matches'))
    teams = Team.query.all()
    return render_template('add_match.html', teams=teams)

def update_ratings(blue_alliance, red_alliance, blue_score, red_score):
    blue_teams = [Team.query.filter_by(name=name.strip()).first() for name in blue_alliance.split(',')]
    red_teams = [Team.query.filter_by(name=name.strip()).
