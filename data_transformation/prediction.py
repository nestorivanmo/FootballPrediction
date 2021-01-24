import pandas as pd
import numpy as np
from data_transformation.data_manipulation.table import Team, ScoreTable, HistoricScoreTable

df = pd.read_csv('../data/england-transformed.csv')
epl_df = pd.read_csv('../data/epl-2020.csv') #english premier league 2020 dataframe matches

def score_season(Season):
    df_season = df[(df.season == Season) & (df.week_day == 38)]

    def teams(name, puntos):
        teams = []
        for nombre, punto in zip(name, puntos):
            teams.append(Team(nombre, punto))
        return teams
        
    home_teams = list(df_season.home)
    home_points = list(df_season.home_current_points)
    visitor_teams = list(df_season.visitor)
    visitor_points = list(df_season.visitor_current_points)

    season_teams = teams(home_teams, home_points) + (teams(visitor_teams,visitor_points))
    score = ScoreTable(season_teams)
    score.sort()
    return score


score_season_2018 = score_season(2018)
score_season_2019 = score_season(2019)

def get_table_position(team, score_table):
    if not score_table.team_exists(team):
        return 21
    position = score_table.get_position(team)
    return position

# Home and visitor position in the last season 
home_last_table_position = []
visitor_last_table_position = []

# Home and visitor position in the penultimate season 
home_penultimate_table_position = []
visitor_penultimate_table_position = []

for index, row in epl_df.iterrows():
    home, visitor = row.home, row.visitor
    home_last_table_position.append(get_table_position(home, score_season_2019))
    visitor_last_table_position.append(get_table_position(visitor, score_season_2019))
    home_penultimate_table_position.append(get_table_position(home, score_season_2018))
    visitor_penultimate_table_position.append(get_table_position(visitor, score_season_2018))

epl_df['home_last_table_position'] = home_last_table_position
epl_df['visitor_last_table_position'] = visitor_last_table_position
epl_df['home_penultimate_table_position'] = home_penultimate_table_position
epl_df['visitor_penultimate_table_position'] = visitor_penultimate_table_position

print(epl_df.head())
print(epl_df.tail())

epl_df.to_csv('../data/england-transformed-2020.csv', index=False)
