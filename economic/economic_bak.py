import numpy as np
import pandas as pd
import pylab as pl
import random, csv
import pudb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from collections import OrderedDict

if __name__ == "__main__":
    with open("CP_inflation.csv") as fh:
        cpi_df = pd.read_csv(file_name, na_values=['-'])
        r = csv.reader(fh, delimiter=',')
        cpi_l = list(filter(lambda x: x[1] == 'USA', r))
        cpi_d = {i: cpi_l[0][i - 1960 + 4] for i in range(1960,2017) }

    with open("WTI.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        # wti_d = {row[0]:row[1] for row in r if '2017' not in row[0] and 'DATE' not in row[0]}
        wti_d = OrderedDict()
        for row in r:
            if '2017' not in row[0] and 'DATE' not in row[0]:
                wti_d[row[0]] = row[1]

    #split data in 70 - 30 sets
    train_size = int(len(wti_d.keys()) * 0.7)
    test_size = len(wti_d.keys()) - train_size

    #merged_d = {date: [cpi_d[int(date[0:4])],wti_d[date]] for date in wti_d.keys()[1:]}
    train_in = []
    train_out = []
    test_in = []
    test_out = []
    for index, date in enumerate(wti_d.keys()):
        if index < train_size:
            train_in.append(cpi_d[int(date[0:4])])
            train_out.append(wti_d[date])
        else:
            test_in.append(cpi_d[int(date[0:4])])
            test_out.append(wti_d[date])

    rf = RandomForestRegressor(n_estimators=50)
    rf.fit(train_in, train_out)
    
    predicted_wti = rf.predict(test_x)

    print("Mean absolute error = {}".format(mean_absolute_error(test_out, predicted_wti)))
    print("Mean squared error = {}".format(mean_squared_error(test_out, predicted_wti)))
    print("R squared = {}".format(r2_score(test_out, predicted_wti)))

    test_out.plot(figsize=(16,12))
    predicted_wti.plot(figsize(16,12))
