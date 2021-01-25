from sklearn.metrics import classification_report

first = lambda x : x[0]
last = lambda x : x[-1]
def compare_tables(teams_real, teams_pred):
    count = 0
    for team in teams_real:
        if team in teams_pred:
            count += 1
    return count / len(teams_real)

def assing_number(arr, champions, relegated):
    results = []
    for i in range(len(arr)):
        number = 2
        if i < champions:
            number = 1
        elif i > len(arr) - relegated:
            number = 3
        row = (arr[i].name, number)
        results.append(row)
    return sorted(results, key = first)

def metrics(score_table_real, score_table_pred, champions = 5, relegated = 3):
    only_first = lambda x : list(map(last, x))
    y_true = only_first(assing_number(score_table_real.teams, champions, relegated))
    y_pred = only_first(assing_number(score_table_pred.teams, champions, relegated))
    # 
    # print(f'Real teams: \t{score_table_real[:champions]}')
    # print(f'Predicted teams: \t{score_table_pred[:champions]}')
    # champions_per = compare_tables(score_table_real[:champions], score_table_pred[:champions])
    # rest_perf = compare_tables(score_table_real[champions:-relegated], score_table_pred[champions:-relegated])
    # relegated_perf = compare_tables(score_table_real[-relegated:], score_table_pred[-relegated:])
    # return (champions_per, rest_perf, relegated_perf)

    return classification_report(y_true, y_pred, labels=[1, 2, 3])