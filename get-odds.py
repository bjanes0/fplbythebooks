import requests
from bs4 import BeautifulSoup
import pandas as pd

data = pd.DataFrame(columns=["name", "goal_percent"])

print("Reading current fixture list...")
fixtures = pd.read_csv('fixtures.csv')

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

data = data.sort_values(by=['goal_percent'], ascending=False)

print("Creating csv of goalscorer odds...")
data.to_csv("goalscorer-percents.csv")
