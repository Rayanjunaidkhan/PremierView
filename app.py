from flask import Flask,render_template,request,redirect,session
import requests
from flask_session import Session
from datetime import datetime,timedelta
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

api_token="e320a275bf3140669260c3aa11f10f1f"
headers = {"X-Auth-Token": api_token}

app = Flask(__name__)
db = SQL("sqlite:///users.db")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.context_processor
def inject_user_status():
    return dict(logged_in=('user_id' in session))

@app.route('/')
def index():
    today = datetime.utcnow().strftime("%Y-%m-%d")
    next_month = (datetime.utcnow() + timedelta(days=30)).strftime("%Y-%m-%d")

    url = f"https://api.football-data.org/v4/competitions/PL/matches?dateFrom={today}&dateTo={next_month}"
    response = requests.get(url, headers=headers)
    data = response.json()

    matches = data.get("matches", [])

    if 'user_id' in session:
        user_id = session['user_id']
        favorite_teams = db.execute("SELECT team_id FROM favorite_teams WHERE user_id = ?", user_id)
        favorite_team_ids = [team['team_id'] for team in favorite_teams]

        favorite_matches = [
            match for match in matches
            if match['homeTeam']['id'] in favorite_team_ids or match['awayTeam']['id'] in favorite_team_ids
        ]

        return render_template("index.html", matches=matches, favorite_matches=favorite_matches)
    else:
        return render_template("index.html", matches=matches, favorite_matches=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not username or not password:
            return "Must provide username and password!"
        if len(user) != 1 or not check_password_hash(user[0]['hash'], password):
            return "Invalid username or password!"
        session['user_id'] = user[0]['id']
        return redirect('/')
    else:
        return render_template("login.html")
    


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmation']
        if not username or not password or not confirm_password:
            return "Must provide all fields!"
        if password != confirm_password:
            return "Passwords do not match!"
        hash_password = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash_password)
        return redirect('/login')
    else:
        return render_template("register.html")
    



@app.route('/favoriteteams', methods=['GET', 'POST'])
@login_required
def favorite_teams():
    if request.method == 'POST':

        team_name = request.form['team_name']
        user_id = session['user_id']
        resp = requests.get("https://api.football-data.org/v4/competitions/PL/teams", headers=headers)
        teams_data = resp.json()

        team_id = None
        for team in teams_data['teams']:
            if team['name'].lower() == team_name.lower():
                team_id = team['id']
                break
            elif team['shortName'].lower() == team_name.lower():
                team_id = team['id']
                break
            elif team['tla'].lower() == team_name.lower():
                team_id = team['id']
                break

        if team_id:
            db.execute("INSERT INTO favorite_teams (user_id, team_id) VALUES (?, ?)", user_id, team_id)
        else:
            return "Team not found!"
        return redirect('/favoriteteams')
    else:
        user_id = session['user_id']
        favorite_teams = db.execute("SELECT team_id FROM favorite_teams WHERE user_id = ?", user_id)
        teams = []
        for team in favorite_teams:
            team_id = team['team_id']
            url = f"https://api.football-data.org/v4/teams/{team_id}"
            response = requests.get(url, headers=headers)
            team_data = response.json()
            teams.append({
            "name": team_data["name"],
            "crest": team_data["crest"]
            })
        return render_template("favoriteteams.html", teams=teams)

@app.route('/remove_team', methods=['POST'])
@login_required
def remove_team():
    team_name = request.form['team_name_remove']
    user_id = session['user_id']
    resp = requests.get("https://api.football-data.org/v4/competitions/PL/teams", headers=headers)
    teams_data = resp.json()

    team_id = None
    for team in teams_data['teams']:
        if team['name'].lower() == team_name.lower():
            team_id = team['id']
            break
        elif team['shortName'].lower() == team_name.lower():
            team_id = team['id']
            break
        elif team['tla'].lower() == team_name.lower():
            team_id = team['id']
            break

    if team_id:
        db.execute("DELETE FROM favorite_teams WHERE user_id = ? AND team_id = ?", user_id, team_id)
    return redirect('/favoriteteams')


@app.route("/player_statistics", methods=["GET", "POST"])
def player_statistics():
    if request.method == "POST":
        player_name = request.form["player_name"]
        resp = requests.get("https://api.football-data.org/v4/competitions/PL/scorers", headers=headers)
        scorers_data = resp.json()

        player_stats = None
        for scorer in scorers_data["scorers"]:
            if  player_name.lower() in scorer["player"]["name"].lower():
                player_stats = {
                    "name": scorer["player"]["name"],
                    "team": scorer["team"]["name"],
                    "goals": scorer["goals"],
                    "assists": scorer.get("assists") or 0,
                    "matches": scorer.get("playedMatches") or 0
                }
                break

        if player_stats:
            return render_template("player_statistics.html", player_stats=player_stats)
        else:
            return "Player not found!"
    else:
        return render_template("player_statistics.html", player_stats=None)
    


@app.route('/table')
def table():
    resp = requests.get("https://api.football-data.org/v4/competitions/PL/standings", headers=headers)
    standings_data = resp.json()

    table = []
    for team in standings_data['standings'][0]['table']:
        table.append({
            "position": team["position"],
            "team": team["team"]["name"],
            "playedGames": team["playedGames"],
            "won": team["won"],
            "draw": team["draw"],
            "lost": team["lost"],
            "points": team["points"],
            "goalsFor": team["goalsFor"],
            "goalsAgainst": team["goalsAgainst"],
            "goalDifference": team["goalDifference"]
        })

    return render_template("table.html", table=table)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')