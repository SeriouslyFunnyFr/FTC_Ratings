from trueskill import Rating, rate

def update_ratings(alliance1_team1_rating, alliance1_team2_rating, alliance2_team1_rating, alliance2_team2_rating, alliance1_score, alliance2_score):
    # Convert ratings to TrueSkill Rating objects
    alliance1 = [Rating(alliance1_team1_rating), Rating(alliance1_team2_rating)]
    alliance2 = [Rating(alliance2_team1_rating), Rating(alliance2_team2_rating)]

    # Update ratings based on the match outcome
    if alliance1_score > alliance2_score:
        new_alliance1, new_alliance2 = rate([alliance1, alliance2], ranks=[0, 1])
    else:
        new_alliance1, new_alliance2 = rate([alliance1, alliance2], ranks=[1, 0])

    # Extract new ratings
    return (
        new_alliance1[0].mu, new_alliance1[1].mu,  # Alliance 1 teams
        new_alliance2[0].mu, new_alliance2[1].mu   # Alliance 2 teams
    )
