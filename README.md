# fplbythebooks
A python application which uses gambling odds to predict Fantasy Premier League points

## How does it work
Every week bookmakers put out gambling odds for the likelihood of each player scoring a goal or a team to keep a clean sheet, and these odds can be converted to percentages. By using these percentages, with the help of the FPL API, fplbythebooks makes a prediction for the number of fantasy points a player will score each matchweek.

## Usage
fplbythebooks is easy to use. Just install the client and neccessary modules to a virtual environment and run. By running the client, it will save csv copies of the fixture list, goalscorer odds, clean sheet odds, and projected points. 

## Notes
The way the script is set up, it only retrieves the "best" odds, meaning that points predictions and goalscorer percents are the total lowest across all bookmakers. 
The program can be used after a matchweek has started, but cannot make predictions for past games once they have been completed.
