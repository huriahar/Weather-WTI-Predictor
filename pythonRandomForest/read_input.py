import pandas as pd
import numpy as np
import random, csv, re
from collections import OrderedDict

# Read CSV file: expects the file to have the name format <city_name>_weather.csv
def read_weather_data (file_name):    
    if not file_name.endswith('.csv'):
        raise ValueError('Expected a .csv extension, but file name is {}'.format(file_name))
    df = pd.read_csv(file_name, na_values=['-', '.'])
    # Extract city name
    city_search = re.search(r'^(\w+)_', file_name)
    city = ""
    if city_search:
        # city will have value in {"houston", "dhahran", "omsk"}
        city = city_search.group(1)
    # Drop source and events attribute in weather table
    df.drop(['source', 'events'], axis = 1, inplace = True)
    # TODO: Find a better way to rename all columns with city names and skipping first column of date
    date_column = df.columns.values[0]
    # Rename all attributes to being city specific
    df = df.add_prefix(city + '_')
    # Rename back the date column
    df.columns.values[0] = date_column
    return df

def read_AAL_csv(file_name):
    df = pd.read_csv(file_name, na_values=['-', '.'])
    df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis = 1, inplace=True)
    df.columns = ['yyyymmdd', 'AAL']
    formatdate = lambda x: int(x[0:4]+x[5:7]+x[8:10])
    roundaal = lambda x: round(x, 2) 
    
    df['yyyymmdd'] = df['yyyymmdd'].map(formatdate)
    df['AAL'] = df['AAL'].map(roundaal)
    #df.replace(r'^\s*$', np.NaN, regex=True, inplace=True)
    return df

def read_world_bank_data_csv(filename, countries):
    min_year = 2007
    max_year = 2017
    df = pd.read_csv(filename, na_values=['-'])
    # filter by country code
    df = df.loc[df['Country Code'].isin(countries)]
    # filter rows
    df.drop(df.ix[:, 'Indicator Name':'2006'], axis=1, inplace=True)
    #df.filter(items=['2007':'2017'])
    return df

def read_gold_data_csv(filename):
    df = pd.read_csv(filename)
    #df.drop(df.index[[0,1,2]], axis=0, inplace=True)
    df.drop(df.ix[:,'USD0':'JPY3'], axis=1, inplace=True)
    df.drop(df.ix[:,'USD5':], axis=1, inplace=True)
    df.columns = ['yyyymmdd', 'gold']
    formatdate = lambda x: int("20"+x[6:8] + x[3:5] + x[0:2])
    df['yyyymmdd'] = df['yyyymmdd'].map(formatdate)
    return df

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

