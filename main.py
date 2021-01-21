import pandas as pd


def read_market_value_csv(location='Data/', season_start=2005, season_end=2020,
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


def get_club_value(club, season):
    """
    Devuelve el valor del equipo dado para la temporada indicada.
    :param club:
    :param season:
    :return:
    """
    market_value_df = read_market_value_csv()
    return market_value_df.loc[(market_value_df.club == club) & (market_value_df.season == season)].market_value


if __name__ == '__main__':
    # football = pd.read_csv('england.csv', low_memory=False)
    # print(football.head())
    # print(football.loc[football.Season == 1888])
    # print(football.loc[(football.Season >= 2005) & (football.division == '1')].home.unique())
    # tm = pd.read_csv('Data/tm-2005-2006.csv')
    # print(tm.head())
    # print(football.loc[(football.home == 'Ipswich Town') & (football.division == 1)])
    print(get_club_value('Chelsea', 2006))
