import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import numpy as np
from pandas.io.json import json_normalize

# Gets recent fixture list from oddschecker.com


def get_fixtures():
    print("Retriving fixture list..")
    url = "https://www.oddschecker.com/football/english/premier-league"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
    linkshtml = requests.get(url, headers=headers).text

    soup = BeautifulSoup(linkshtml, 'html5lib')

    data = pd.DataFrame(columns=["event", "link"])

    a_tag = soup.findAll(
        'a', class_='beta-callout full-height-link whole-row-link')

    i = 0

    print("Parsing next 10 fixtures (1 gameweek)...")
    for tag in a_tag:
        df = pd.DataFrame({"event": [tag["data-event-name"]],
                           "link": ["https://www.oddschecker.com/" + tag["href"][:-6]]}, index=[i])
        data = data.append(df)
        i += 1
        if i == 10:
            break

    print("Creating csv of fixture list...")
    data.to_csv("fixtures.csv")

    return data


def get_odds(fixtures):
    data = pd.DataFrame(columns=["name", "goal_percent"])

    print("Reading current fixture list...")
    #fixtures = pd.read_csv('fixtures.csv')

    print("Retrieving player odds from fixtures...")
    for index, row in fixtures.head(n=10).iterrows():
        url = row['link'] + "anytime-goalscorer"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        html = requests.get(url, headers=headers).text

        soup = BeautifulSoup(html, 'html5lib')

        tr_tag = soup.find_all('tr', class_='diff-row evTabRow bc')

        i = 0
        for tag in tr_tag:
            df = pd.DataFrame({"name": [tag["data-bname"]],
                               "goal_percent": [int(1/float(tag["data-best-dig"])*100)]}, index=[i])
            data = data.append(df)
            i += 1

    if data.empty:
        print("Error: Goalscorer odds not yet available")
        sys.exit()

    data = data.sort_values(by=['goal_percent'], ascending=False)

    print("Creating csv of goalscorer odds...")
    data.to_csv("goalscorer-percents.csv")

    return data

# Retrives json from api and writes to output file


def get_data(file_path):
    r = requests.get(
        'https://fantasy.premierleague.com/api/bootstrap-static/')
    return r.json()

# Retrieves correct element from FPL API


def get_players(json):
    return pd.io.json.json_normalize(json, ['elements'])


print("Retrieving bootstrap-static from FPL API...")
dataJSON = get_data("bootstrap-static.json")

print("Parsing players...")
players = get_players(dataJSON)

# Update the fixture list
fixtures = get_fixtures()

# Get player odds using most recent fixtures
sample = get_odds(fixtures)

# Parse only the relevant data from the FPl API
players = players[['id', 'first_name',
                   'second_name', 'element_type', 'now_cost', 'team_code']]
players['name'] = players['first_name'] + " " + players["second_name"]
players = players.drop(columns=['first_name', 'second_name'])

# Retrieve recent bookmaker data
#sample = pd.read_csv("goalscorer-percents.csv")
df = pd.merge(sample, players)

# Remove previous indeces

# Set conditions depending on player position
conditions = [(df['element_type'] == 1) | (df['element_type'] == 2),
              df['element_type'] == 3, df['element_type'] == 4]
choices = [(((df['goal_percent']/100) * 6) + 2),
           (((df['goal_percent']/100) * 5) + 2), ((df['goal_percent']/100) * 4) + (2)]

# Evaluate projected points based on odds
df['projected_points'] = np.select(conditions, choices)

df = df.sort_values(by=['projected_points'], ascending=False)

print("Exporting projected points to csv...")
df.to_csv("projected_points.csv")
