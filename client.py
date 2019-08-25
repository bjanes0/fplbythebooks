import pandas as pd
import requests
import json
import numpy as np
from pandas.io.json import json_normalize

# Function retrives json from api and writes to output file


def get_data(file_path):
    r = requests.get(
        'https://fantasy.premierleague.com/api/bootstrap-static/')
    return r.json()

# Function retrieves correct element from FPL API


def get_players(json):
    return pd.io.json.json_normalize(json, ['elements'])


print("Retrieving bootstrap-static from FPL API...")
dataJSON = get_data("bootstrap-static.json")

print("Parsing players...")
players = get_players(dataJSON)

# Parse only the relevant data from the FPl API
players = players[['id', 'first_name',
                   'second_name', 'element_type', 'now_cost', 'team_code']]
players['name'] = players['first_name'] + " " + players["second_name"]
players = players.drop(columns=['first_name', 'second_name'])

# Retrieve recent bookmaker data
sample = pd.read_csv("goalscorer-percents.csv")
df = pd.merge(sample, players)

# Remove previous indeces
df = df.drop(df.columns[0], axis=1)

# Set conditions depending on player position
conditions = [(df['element_type'] == 1) | (df['element_type'] == 2),
              df['element_type'] == 3, df['element_type'] == 4]
choices = [(((df['goal_percent']/100) * 6) + 2),
           (((df['goal_percent']/100) * 5) + 2), ((df['goal_percent']/100) * 4) + (2)]

# Evaluate projected points based on odds
df['projected_points'] = np.select(conditions, choices)

df = df.sort_values(by=['projected_points'], ascending=False)

print("Exporting projected points to csv")
df.to_csv("projected_points.csv")
