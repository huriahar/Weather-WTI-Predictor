import numpy as np
import pandas as pd
import pylab as pl
import random, csv
import pudb
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from collections import OrderedDict


if __name__ == "__main__":
    ################################ input formatting ####################################
    with open("gold_prices.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        gold_l = [row for row in r]
        gold_l = gold_l[1:]
        gold_l = list(filter(lambda x: int(x[0][0:4]) >= 2007, gold_l))
        gold_d = {d[0]: d[1] for d in gold_l }

    with open("Interest_rate.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        ir_l = list(filter(lambda x: x[1] == 'USA', r))
        ir_d = {i: ir_l[0][i - 1960 + 4] for i in range(1960,2014) }

    with open("GDP.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        gdp_l = list(filter(lambda x: x[1] == 'USA', r))
        gdp_d = {i: gdp_l[0][i - 1960 + 4] for i in range(1960,2014) }

    with open("CP_inflation.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        cpi_l = list(filter(lambda x: x[1] == 'USA', r))
        cpi_d = {i: cpi_l[0][i - 1960 + 4] for i in range(1960,2014) }

    with open("WTI.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        # wti_d = {row[0]:row[1] for row in r if '2017' not in row[0] and 'DATE' not in row[0]}
        wti_d = OrderedDict()
        for row in r:
            if 'DATE' not in row[0] and int(row[0][0:4]) < 2014:
                wti_d[row[0]] = row[1]

    with open("merged.csv", "wb") as fh:
        csv_writer = csv.writer(fh, delimiter=',')
        csv_writer.writerow(['idx',"gold", "ir", "cpi", "gdp", "wti"])
        for index, date in enumerate(wti_d.keys()):
            gld = gold_d[date[0:8] + '01']
            ir  = ir_d[int(date[0:4])]
            cpi = cpi_d[int(date[0:4])]
            gdp = gdp_d[int(date[0:4])]
            wti = wti_d[date]
            csv_writer.writerow([index, gld, ir, cpi, gdp, wti])

    ##################################### training  #########################################
    #split data in 70 - 30 sets
    train_size = int(len(wti_d.keys()) * 0.7)
    test_size = len(wti_d.keys()) - train_size

    merged_df = pd.read_csv("merged.csv", na_values=['-', '.'])
    merged_df.fillna(merged_df.mean()['gold':'wti'], inplace=True)
    train, test = merged_df[0:train_size], merged_df[train_size:]


    train_in, train_out = train.iloc[:,1:2], train.iloc[:,-1]
    test_in, test_out = test.iloc[:,1:2], test.iloc[:,-1]

    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(train_in, train_out)

    ##################################### testing ##########################################
    test['predicted_wti'] = rf.predict(test_in)

    print("Mean absolute error = {}".format(mean_absolute_error(test_out, test['predicted_wti'])))
    print("Mean squared error = {}".format(mean_squared_error(test_out, test['predicted_wti'])))
    print("R squared = {}".format(r2_score(test_out, test['predicted_wti'])))

    #test['wti'].plot(figsize=(16,12))
    #test['predicted_wti'].plot(figsize(16,12))

    #pl.scatter(test_out, test['predicted_wti'])
    #pl.plot()
    #pl.show()

    #merged_df.plot(x='idx', y='wti', style='o')
    #test.plot(x='idx', y='wti', style='o')
    #test.plot(y='predicted_wti', use_index=True)

    test['idx'] = test['idx'][:-200]

    pl.scatter(test['idx'], test['wti'])
    pl.scatter(test['idx'], test['predicted_wti'])
    pl.xlabel('Date')
    pl.ylabel('Oil prices')
    pl.show()

