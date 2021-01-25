import pandas as pd
import numpy as np


def read_market_value_csv(location='../data/data_money/', season_start=2005, season_end=2020,
                          col_names=['club', 'squad_size', 'avg_age', 'num_foreigners', 'market_value',
                                     'av_market_value']):
    """
    Devuelve un DataFrame que contiene el valor estimado de los equipos por temporada.
    :param location:
    :param season_start:
    :param season_end:
    :param col_names:
    :return:
    """
    market_value = pd.DataFrame(columns=col_names)
    for season in range(season_start, season_end + 1):
        temp_df = pd.read_csv(location + 'tm-' + str(season) + '-' + str(season + 1) + '.csv')
        temp_df['season'] = season
        market_value = pd.concat(
            [market_value, temp_df])
    return market_value


teams = pd.read_csv('../data/teams.csv')
market_value_df = read_market_value_csv()


def get_club_value(club_index, season):
    """
    Devuelve el valor del equipo dado para la temporada indicada.
    :param club_index:
    :param season:
    :return:
    """
    club = teams[teams.team_number == club_index].team_name.values[0]
    return market_value_df.loc[(market_value_df.club == club) &
                               (market_value_df.season == season)].market_value.values[0]


df = pd.read_csv('../data/england-transformed-2020.csv')
df = df[df.season >= 2005]
h_team_val = []
v_team_val = []
for index, row in df.iterrows():
    h_team_val.append(get_club_value(row.home, row.season))
    v_team_val.append(get_club_value(row.visitor, row.season))
df['home_value'] = h_team_val
df['visitor_value'] = v_team_val
df = df.reindex(columns=['season', 'week_day', 'year', 'month', 'day', 'home', 'visitor',
                         "home_current_points", "visitor_current_points", "home_last_table_position",
                         "visitor_last_table_position", "home_penultimate_table_position",
                         "visitor_penultimate_table_position", "home_value", "visitor_value", "result"])
df.to_csv('../data/england-transformed-2020.csv', index=False)
