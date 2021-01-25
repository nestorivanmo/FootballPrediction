from os import name
import pandas as pd
import numpy as np
from score_table.table import Team, ScoreTable, HistoricScoreTable
from score_table.create import score_season
from team_value import set_value

if __name__ == '__main__':

    df = pd.read_csv('../data/england-transformed.csv')
    epl_df = pd.read_csv('../data/epl-2020.csv') #english premier league 2020 dataframe matches

    score_season_2018 = score_season(df, 2018)
    score_season_2019 = score_season(df, 2019)

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
    
    wp = rp = '../data/england-transformed-2020.csv'
    set_value(wp, rp)
