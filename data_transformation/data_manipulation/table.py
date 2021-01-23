from functools import total_ordering
import numpy as np

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
        
class ScoreTable:  # Revisar por el cambio ndarray
    """
    A class for storing the Team's positions based on the current position.
    """
    @staticmethod
    def __indice__(arr, value):
        try:
            return np.where(arr == int(value))[0][0]            
        except:
            print("hola")
            print(arr)
            print(value)
            exit(-1)
        
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
    def __init__(self, name, points = 0):
        self.name = name
        self.points = points
    
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
            return self.points == other.points
        elif type(self.name) == str and type(other) == str:
            return self.name == other
        elif type(self.name) in (int, np.int64)  and type(other) in (int, np.int64):
            return np.int64(self.name) == np.int64(other)
        return None

    def __str__(self):
        return "%d - %d" % (self.name, self.points)

    def __repr__(self):
        return "Team(name: %d, points: %d)" % (self.name, self.points)
