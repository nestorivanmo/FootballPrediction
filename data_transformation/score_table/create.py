from table import *
import pandas as pd
import numpy as np

def score_season(df, Season):
    df_temp = df[df.season == Season]
    last_week_day = int(df_temp.week_day.max())
    df_season = df[(df.season == Season) & (df.week_day == last_week_day)]

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

def prediction_score_table(model, df, verbose = False):
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
            if result == 1: # if a draw
                teams_table.add_points(home, 1)
                teams_table.add_points(visitor, 1)
            else:
                winner, loser = home, visitor
                if result == 3: # if visitor win
                    winner, loser = visitor, home
                teams_table.add_points(winner, 3)
        teams_table.sort()

    winner = teams_table.teams[0].from_number_to_team().name.capitalize()
    teams_table.teams = [Team(name_team.get(team.name), team.points) for team in teams_table.teams]
    teams_table.sort()
    if verbose: 
        print("And the winner is:")
        print(winner)
        print("The table score is:")
        print(teams_table)
    return winner, teams_table