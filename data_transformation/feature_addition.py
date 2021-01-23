"""
Feature addition to the dataset. Features such as current points in the table,
last position in the table and penultime position in the table. This features
apply both to home and visitor. 
"""

import pandas as pd
import numpy as np 
from data_manipulation.table import Team, ScoreTable, HistoricScoreTable 

df = pd.read_csv("../data/england-clean.csv")

# Home and visitor current points in the score table
home_current_points = []
visitor_current_points = []

# Home and visitor position in the last season 
home_last_table_position = []
visitor_last_table_position = []

# Home and visitor position in the penultimate season 
home_penultimate_table_position = []
visitor_penultimate_table_position = []

historic_score_table = HistoricScoreTable()

seasons_max = df.season.max()
seasons_min = df.season.min()
for season in range(seasons_min, seasons_max + 1):
    season_df = df[df.season == season]

    teams = list(season_df.home.unique())
    teams_table = ScoreTable([Team(team) for team in teams])

    weeks = season_df.week_day.max()
    for week in range(1, weeks + 1):
        match_df = season_df[season_df.week_day == week]
        for index, row in match_df.iterrows():
            home, visitor = row.home, row.visitor
            if row.result == 1: # if a draw
                teams_table.add_points(home, 1)
                teams_table.add_points(visitor, 1)
            else:
                winner, loser = home, visitor
                if row.result == 3: # if visitor win
                    winner, loser = visitor, home
                teams_table.add_points(winner, 3)

            # Adding current points
            home_current_points.append(teams_table.get_points(home))
            visitor_current_points.append(teams_table.get_points(visitor))
            home_last_table_position.append(
                historic_score_table.get_last_posititon(home)
            )
            visitor_last_table_position.append(
                historic_score_table.get_last_posititon(visitor)
            )
            home_penultimate_table_position.append(
                historic_score_table.get_penultimate_posititon(home)
            )
            visitor_penultimate_table_position.append(
                historic_score_table.get_penultimate_posititon(visitor)
            )
        teams_table.sort()
    historic_score_table += teams_table

df['home_current_points'] = home_current_points
df['visitor_current_points'] = visitor_current_points
df['home_last_table_position'] = home_last_table_position
df['visitor_last_table_position'] = visitor_last_table_position
df['home_penultimate_table_position'] = home_penultimate_table_position
df['visitor_penultimate_table_position'] = visitor_penultimate_table_position

df = df.reindex(columns= ['season', 'week_day', 'year', 'month', 'day', 'home','visitor', 
                    "home_current_points","visitor_current_points","home_last_table_position",
                    "visitor_last_table_position","home_penultimate_table_position",
                    "visitor_penultimate_table_position", "result"])
df.to_csv('../data/england-transformed.csv', index=False)

