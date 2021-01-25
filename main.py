import pandas as pd
from team_value import team_value

if __name__ == '__main__':
    # football = pd.read_csv('data/england.csv', low_memory=False)
    # print(football.head())
    # print(football.loc[football.Season == 1888])
    # print(football.loc[(football.Season >= 2005) & (football.division == '1')].home.unique())
    # tm = pd.read_csv('data/data_money/tm-2005-2006.csv')
    # print(tm.head())
    # print(football.loc[(football.home == 'Ipswich Town') & (football.division == 1)])
    # print(team_value.get_club_value(1, 2019))
    for i in range(2005, 2020):
        for j in range(1, 53):
            team_value.get_club_value(j, i)

