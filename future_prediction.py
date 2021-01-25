from os import name
import pandas as pd
import numpy as np
import pickle
from data_transformation.score_table.table import ScoreTable, Team
from data_transformation.score_table.create import prediction_score_table

if __name__ == '__main__':

    pkl_filename = "model.pkl"
    with open(pkl_filename, 'rb') as file:
        model = pickle.load(file)

    df = pd.read_csv("data/england-transformed-2020.csv")
    prediction_score_table(model, df, True)
