import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from data_transformation.score_table.create import prediction_score_table, score_season
from data_transformation.score_table.table import *
from data_transformation.score_table.metrics import metrics

pkl_filename = "model.pkl"
with open(pkl_filename, 'rb') as file:
    model = pickle.load(file)

football = pd.read_csv('data/england-transformed.csv')

seasons = football.season.values
seasons_unique = football.season.unique()

X = football.iloc[:, :-1].values
y = football.iloc[:, -1].values

scaler = StandardScaler()
X = scaler.fit_transform(X)

def concat_final(df, arr, arr_name='result'):
    df[arr_name] = arr
    return df

tcsv = TimeSeriesSplit(n_splits=5)

for train_season_index, test_season_index in tcsv.split(seasons_unique):
    train_season = seasons_unique[train_season_index] 
    test_season = seasons_unique[test_season_index]
    train_index = np.isin(seasons, train_season)
    test_index = np.isin(seasons, test_season)

    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    for s in test_season:
        test_index = np.isin(seasons, s)
        y_real = score_season(football, s)
        _, y_pred = prediction_score_table(model, football.iloc[test_index, :-1])
        y_real.from_number_to_team()
        # print(y_real)
        # print(y_pred)
        a_metric = metrics(y_real, y_pred) 
        print("{} - \n{}\n".format(s, a_metric))

