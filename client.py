import pandas as pd
import requests
import json
import numpy as np
from pandas.io.json import json_normalize

"""Function retrives json from api and writes to output file"""


def get_data(file_path):
    r = requests.get(
        'https://fantasy.premierleague.com/api/bootstrap-static/')
    return r.json()


def get_players(json):
    return pd.io.json.json_normalize(json, ['elements'])


print("Retrieving bootstrap-static from FPL API...")
dataJSON = get_data("bootstrap-static.json")

print("Parsing players...")
players = get_players(dataJSON)

# Parse only the relevant data
players = players[['id', 'first_name',
                   'second_name', 'element_type', 'now_cost']]

# Retrieve recent bookmaker data
sample = pd.read_csv("sample_data.csv")
df = pd.merge(sample, players)

# Set conditions depending on player position
conditions = [df['element_type'] == 1 | df['element_type'] == 2,
              (df['element_type'] == 3), (df['element_type'] == 4)]
choices = [((df['goal_odds'] * 6) + (df['assist_odds'] * 3) + (df['cs_odds'] * 4) + 2), ((df['goal_odds'] * 5) + (
    df['assist_odds'] * 3) + (df['cs_odds'] * 1) + 2), ((df['goal_odds'] * 4) + (
        df['assist_odds'] * 3) + 2)]

# Evaluate projected points based on
df['projected_points'] = np.select(conditions, choices)
print(df)
df.to_csv("projected_points.csv")
