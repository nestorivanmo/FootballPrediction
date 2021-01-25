from functools import total_ordering
import numpy as np


def compare_tables(teams_real, teams_pred):
    count = 0
    for team in teams_real:
        if team in teams_pred:
            count += 1
    return count / len(teams_real)

def metrics(score_table_real, score_table_pred, champions = 5, relegated = 3):
    score_table_real = score_table_real.teams
    score_table_pred = score_table_pred.teams
    # print(f'Real teams: \t{score_table_real[:champions]}')
    # print(f'Predicted teams: \t{score_table_pred[:champions]}')
    champions_per = compare_tables(score_table_real[:champions], score_table_pred[:champions])
    rest_perf = compare_tables(score_table_real[champions:-relegated], score_table_pred[champions:-relegated])
    relegated_perf = compare_tables(score_table_real[-relegated:], score_table_pred[-relegated:])
    return (champions_per, rest_perf, relegated_perf)
    
    
class HistoricScoreTable:
    def __init__(self):
        self.last = None
        self.penultimate = None

    def __add__(self, other):
        """
        a: HistoricScoreTable
        b: ScoreTable
        new: HistoricScoreTable
        """
        new = HistoricScoreTable()
        new.last = other
        new.penultimate = self.last
        return new

    @staticmethod
    def get_points(team, score_table, v = -1):
        if score_table is None or not score_table.team_exists(team):
            return v
        return score_table.get_points(team)
    
    @staticmethod
    def get_position(team, score_table, v = -1):
        if score_table is None:
            return 42
        if not score_table.team_exists(team):
            return len(score_table) + 1
        return score_table.get_position(team)

    def get_last_points(self, team):
        return HistoricScoreTable.get_points(team, self.last)
    
    def get_penultimate_points(self, team):
        return HistoricScoreTable.get_points(team, self.penultimate)

    def get_last_posititon(self, team):
        return HistoricScoreTable.get_position(team, self.last)
    
    def get_penultimate_posititon(self, team):
        return HistoricScoreTable.get_position(team, self.penultimate)


    def __str__(self):
        return "Last:\n%s\n\nPenultimate:\n%s" %(str(self.last), str(self.penultimate))
    
    def __repr__(self):
        return "HistoricScoreTable(Last:\n%s\n\nPenultimate:\n%s)" %(repr(self.last), repr(self.penultimate)) 
        
class ScoreTable:  
    """
    A class for storing the Team's positions based on the current position.
    """
    @staticmethod
    def __indice__(arr, value):
        return np.where(arr == int(value))[0][0]            
        
    def __init__(self, teams):
        self.teams = np.array(teams)
    
    def get_position(self, team):  
        indice = ScoreTable.__indice__(self.teams, team)
        return indice + 1

    def get_points(self, team):
        indice = ScoreTable.__indice__(self.teams, team)
        return self.teams[indice].points

    def add_points(self, team, points):
        indice = ScoreTable.__indice__(self.teams, team)
        self.teams[indice] += points

    def team_exists(self, team):
        return team in self.teams

    def from_number_to_team(self):
        for i in range(len(self.teams)):
            self.teams[i].from_number_to_team()
    
    def from_team_to_number(self):
        for i in range(len(self.teams)):
            self.teams[i].from_team_to_number()

    def sort(self):
        self.teams.sort()
        self.teams = self.teams[::-1]

    def __len__(self):
        return len(self.teams)

    def __str__(self): 
        return "\n".join("%d. %s" % (i + 1, str(team)) for i, team in enumerate(self.teams))

    def __repr__(self):
        return "ScoreTable(%s)" % "\n".join("%d. %s" % (i + 1, str(team)) for i, team in enumerate(self.teams))

@total_ordering
class Team:
    """
    A class that contains the data for each team.
    """
    dict_team = {'AFC Bournemouth': 0,
        'Arsenal': 1,
        'Aston Villa': 2,
        'Barnsley': 3,
        'Birmingham City': 4,
        'Blackburn Rovers': 5,
        'Blackpool': 6,
        'Bolton Wanderers': 7,
        'Bradford City': 8,
        'Brighton & Hove Albion': 9,
        'Burnley': 10,
        'Cardiff City': 11,
        'Charlton Athletic': 12,
        'Chelsea': 13,
        'Coventry City': 14,
        'Crystal Palace': 15,
        'Derby County': 16,
        'Everton': 17,
        'Fulham': 18,
        'Huddersfield Town': 19,
        'Hull City': 20,
        'Ipswich Town': 21,
        'Leeds United': 22,
        'Leicester City': 23,
        'Liverpool': 24,
        'Luton Town': 25,
        'Manchester City': 26,
        'Manchester United': 27,
        'Middlesbrough': 28,
        'Millwall': 29,
        'Newcastle United': 30,
        'Norwich City': 31,
        'Nottingham Forest': 32,
        'Notts County': 33,
        'Oldham Athletic': 34,
        'Oxford United': 35,
        'Portsmouth': 36,
        'Queens Park Rangers': 37,
        'Reading': 38,
        'Sheffield United': 39,
        'Sheffield Wednesday': 40,
        'Southampton': 41,
        'Stoke City': 42,
        'Sunderland': 43,
        'Swansea City': 44,
        'Swindon Town': 45,
        'Tottenham Hotspur': 46,
        'Watford': 47,
        'West Bromwich Albion': 48,
        'West Ham United': 49,
        'Wigan Athletic': 50,
        'Wimbledon': 51,
        'Wolverhampton Wanderers': 52}
    def __init__(self, name, points = 0):
        self.name = name
        self.points = points
    
    def from_number_to_team(self):
        dict_team = dict(zip(Team.dict_team.values(), Team.dict_team.keys()))
        self.name = dict_team.get(self.name)
    
    def from_team_to_number(self):
        self.name = Team.dict_team.get(self.name)

    def __add__(self, other):
        return Team(self.name, self.points + other)

    def __lt__(self, other):
        if type(other) == Team:
            return self.points < other.points
        elif type(other) == str:
            return self.name < other
        return None

    def __eq__(self, other):
        if type(other) == Team:
            return self.name == other.name or self.points == other.points
        elif type(self.name) == str and type(other) == str:
            return self.name == other
        elif type(self.name) in (int, np.int64)  and type(other) in (int, np.int64):
            return np.int64(self.name) == np.int64(other)
        return None

    def __str__(self):
        return "%s - %d" % (str(self.name), self.points)

    def __repr__(self):
        return "Team(name: %s, points: %d)" % (str(self.name), self.points)
