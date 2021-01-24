import pandas as pd
import numpy as np
import pickle
from data_transformation.data_manipulation.table import ScoreTable, Team

pkl_filename = "model.pkl"
with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)

df = pd.read_csv("data/england-transformed-2020.csv")

teams = list(df.home.unique())
teams_table = ScoreTable([Team(team) for team in teams])

weeks = df.week_day.max()
for week in range(1, weeks + 1):
    match_df = df[df.week_day == week]
    for index, row in match_df.iterrows():
        home, visitor = row.home, row.visitor
        home_current_points = teams_table.get_points(home)
        visitor_current_points = teams_table.get_points(visitor)
        result = model.predict([[row.season, row.week_day, row.year,
                                 row.month, row.day,
                                 home, visitor,
                                 home_current_points,
                                 visitor_current_points,
                                 row.home_last_table_position,
                                 row.visitor_last_table_position,
                                 row.home_penultimate_table_position,
                                 row.visitor_penultimate_table_position,
                                 row.home_value,
                                 row.visitor_value]])
        if result == 1:  # if a draw
            teams_table.add_points(home, 1)
            teams_table.add_points(visitor, 1)
        else:
            winner, loser = home, visitor
            if result == 3:  # if visitor win
                winner, loser = visitor, home
            teams_table.add_points(winner, 3)
    teams_table.sort()

winner = teams_table.teams[0].name
teams = pd.read_csv("data/teams.csv")
name_team = dict(zip(teams.team_number, list(teams.team_name)))

print("And the winner is:")
print(name_team.get(winner).capitalize())

print("The table score is:")
teams_table.teams = [Team(name_team.get(team.name), team.points) for team in teams_table.teams]
teams_table.sort()
print(teams_table)
