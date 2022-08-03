import os
import requests
import json

from requests.api import get
from dotenv import load_dotenv

load_dotenv()
odds_api_key = os.environ.get("ODDS_API_KEY")
league = os.environ.get("ODDS_API_LEAGUE")
mock_requests = os.environ.get("ODDS_API_MOCK_RESPONSE")

def get_mocked_json():
    mocked_json_file = open("sample_odds.json", 'r')
    contents = json.loads(mocked_json_file.read())
    return contents

def get_odds_moneyline(home_team, away_team, result):
    route = "https://api.the-odds-api.com/v4/sports/{}/odds?regions=us&apiKey={}&markets=h2h".format(league, odds_api_key)

    if mock_requests:
        matches = get_mocked_json()
    else:
        matches = requests.request(
            "GET",
            route,
        ).json()

    books = None
    for match in matches:
        if match['home_team'] == home_team and match['away_team'] == away_team: 
            books = match['bookmakers']
            break
    if books is None: return None

    markets = None
    for book in books:
        if book['key'] == "draftkings": 
            markets = book['markets']
            break
    if markets is None: return None

    moneyline_odds = None
    for market in markets:
        if market['key'] == "h2h": 
            moneyline_odds = market['outcomes']
            break
    if moneyline_odds is None: return None

    for odds in moneyline_odds:
        if odds['name'] == result: return odds['price']
    return None

print(get_odds_moneyline("Watford", "Liverpool", "Watford"))




    

