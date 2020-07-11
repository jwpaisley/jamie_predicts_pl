import requests
import time
import os
import math
from datetime import datetime, timedelta, timezone
from dateutil import parser
from dotenv import load_dotenv
from team import Team
from twitter import TwitterClient
from utils import headers

twitter_client = TwitterClient()
load_dotenv()
LEAGUE_ID = os.getenv("LEAGUE_ID")

def get_utc_timestamp():
    return int(datetime.utcnow().timestamp())

def current_utc_day():
    return datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0) 

def seconds_to(time):
    return int((time - datetime.utcnow()).total_seconds())

def get_league_averages(league_results):
    home_goals, away_goals = 0.0, 0.0
    for result in league_results:
        home_goals += result['goalsHomeTeam']
        away_goals += result['goalsAwayTeam']

    return { 
        'home_goals': home_goals / len(league_results), 
        'away_goals': away_goals / len(league_results) 
    }

def get_results_for_league(league_id):
    results = requests.request(
        "GET", 
        "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/{lid}".format(lid=league_id), 
        headers=headers
    ).json()['api']['fixtures']

    return results

def get_fixtures_by_day(league_id, day):
    route = "https://api-football-v1.p.rapidapi.com/v2/fixtures/league/524/{date}".format(date=day)
    fixtures = requests.request(
        "GET", 
        route,
        headers=headers
    ).json()['api']['fixtures']

    return fixtures

def predict_goals(attack, defense, average):
    rel_atk = attack / average
    rel_def = defense / average
    return average * rel_atk * rel_def

def make_prediction(delay, fixture):
    time.sleep(delay)
    
    home_team = Team(fixture['homeTeam']['team_id'], fixture['homeTeam']['team_name'])
    away_team = Team(fixture['awayTeam']['team_id'], fixture['awayTeam']['team_name'])

    home_goals = predict_goals(home_team.home_atk, away_team.away_def, league_averages['home_goals'])
    away_goals = predict_goals(away_team.away_atk, home_team.home_def, league_averages['away_goals'])

    pred_home_goals = expected_value(home_goals)
    pred_away_goals = expected_value(away_goals)

    prediction = 'Prediction: {} {}, {} {}'.format(
        home_team.name, 
        pred_home_goals, 
        away_team.name, 
        pred_away_goals
    )
    # twitter_client.tweet(prediction)
    print(prediction)

def poisson(mu, x):
    return ((2.71828**(-1*mu))*(mu**x))/(math.factorial(x))

def expected_value(mu):
    poisson_list = []
    for i in range(0, 6):
        P = poisson(mu, i)
        poisson_list.append(P)
    return poisson_list.index(max(poisson_list))

league_results = get_results_for_league(LEAGUE_ID)
league_averages = get_league_averages(league_results)
league_averages = {'away_goals': 1.2526315789473683, 'home_goals': 1.568421052631579}
fixtures = get_fixtures_by_day(542, current_utc_day().strftime('%Y-%m-%d'))

for fixture in fixtures:
    delay = datetime.strptime(fixture['event_date'], "%Y-%m-%dT%H:%M:%S+00:00") - timedelta(minutes=15)
    make_prediction(delay, fixture)