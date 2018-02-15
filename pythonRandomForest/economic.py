import random, csv
from collections import OrderedDict
import pandas as pd

def get_economic_data():

    with open("gold_prices.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        gold_l = [row for row in r]
        gold_l = gold_l[1:]
        gold_l = list(filter(lambda x: int(x[0][0:4]) >= 2007, gold_l))
        gold_d = {d[0]: d[1] for d in gold_l }

    with open("Interest_rate.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        ir_l = list(filter(lambda x: x[1] == 'USA', r))
        ir_d = {i: ir_l[0][i - 1960 + 4] for i in range(2007,2014) }

    with open("GDP.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        gdp_l = list(filter(lambda x: x[1] == 'USA', r))
        gdp_d = {i: gdp_l[0][i - 1960 + 4] for i in range(2007,2014) }

    with open("CP_inflation.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        cpi_l = list(filter(lambda x: x[1] == 'USA', r))
        cpi_d = {i: cpi_l[0][i - 1960 + 4] for i in range(2007,2014) }

    with open("WTI.csv") as fh:
        r = csv.reader(fh, delimiter=',')
        # wti_d = {row[0]:row[1] for row in r if '2017' not in row[0] and 'DATE' not in row[0]}
        wti_d = OrderedDict()
        for row in r:
            if 'DATE' not in row[0] and int(row[0][0:4]) < 2014:
                wti_d[row[0]] = row[1]

    with open("merged.csv", "wb") as fh:
        csv_writer = csv.writer(fh, delimiter=',')
        csv_writer.writerow(['yyyymmdd',"gold", "ir", "cpi", "gdp", "wti"])
        for index, date in enumerate(wti_d.keys()):
            gld = gold_d[date[0:8] + '01']
            ir  = ir_d[int(date[0:4])]
            cpi = cpi_d[int(date[0:4])]
            gdp = gdp_d[int(date[0:4])]
            wti = wti_d[date]
            csv_writer.writerow([int(date[0:4]+date[5:7]+date[8:10]), gld, ir, cpi, gdp, wti])

    train_size = int(len(wti_d.keys()) * 0.7)
    test_size = len(wti_d.keys()) - train_size

    merged_df = pd.read_csv("merged.csv", na_values=['-', '.'])
    merged_df.fillna(merged_df.mean()['gold':'wti'], inplace=True)
    return merged_df
