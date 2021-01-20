import pandas as pd

if __name__ == '__main__':
    football = pd.read_csv('english.csv', low_memory=False)
    print(football.head())
