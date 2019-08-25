import requests
from bs4 import BeautifulSoup
import pandas as pd

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

print("Parsing...")
for tag in a_tag:
    df = pd.DataFrame({"event": [tag["data-event-name"]],
                       "link": ["https://www.oddschecker.com/" + tag["href"][:-6]]}, index=[i])
    data = data.append(df)
    i += 1
    if i == 10:
        break

print("Creating csv of fixture list...")
data.to_csv("fixtures.csv")
