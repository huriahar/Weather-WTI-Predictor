import numpy as np
import pandas as pd
import pylab as pl
import random, csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

with open("houston.csv") as fh:
    r = csv.reader(fh, delimiter=',')
    dict1 = {row[1]: row[2:] for row in r}

with open("WTI.csv") as fh:
    r = csv.reader(fh, delimiter=',')
    dict2 = {row[0]: row[1] for row in r}

with open("merged.csv", 'wb') as fh:
    w = csv.writer(fh, delimiter=',')
    # Write the column names to the CSV file
    row = ["Date"]
    row.extend(dict1["Date"])
    row.append("WTI")
    w.writerow(row)

    for key in dict2.keys():
        row = []
        if key in dict1:
            row.append(key)
            row.extend(dict1[key])
            row.append(dict2[key])
            w.writerow(row)

df = pd.read_csv("merged.csv", na_values=['.', 'T', '""'])
df = df.fillna(df.mean())
print(df['Mean.Humidity'].corr(df['WTI']))
np.random.seed(200)
train = df.sample(frac=0.75)
test = df.drop(train.index)

train_x, train_y = train.iloc[:, 1:21], train.iloc[:, -1]
test_x, test_y = test.iloc[:, 1:21], test.iloc[:, -1]

rf = RandomForestRegressor(n_estimators=20)

rf.fit(train_x, train_y)
pred = rf.predict(test_x)

print("Mean Absolute Error:", mean_absolute_error(test_y, pred))
print("Mean Squared Error:", mean_squared_error(test_y, pred))
r2=r2_score(test_y, pred)
print("R squared:", r2)

pl.scatter(test_y, pred)
pl.plot(np.arange(1, 120), np.arange(1, 120), label="r^2=" + str(r2), c="r")
pl.legend(loc="lower right")
pl.title("RandomForest Regression with scikit-learn")
pl.show()
