import datetime
import pandas as pd
import numpy as np
import re, argparse
import pylab as pl
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.cross_validation import train_test_split
from economic import get_economic_data
import pudb

def date_time_to_str(d):
    d = str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2)
    return d

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

def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--future', nargs='?', const=0, type=int, default=0, required=True,
                        help="Add the number of days from the given day that you wish to make the prediction for")
    parser.add_argument('-d', '--date', nargs='?', const=0, type=int, default=0, required=True,
                        help="Enter date in format yyyymmdd. Starting from this date..predict")
    parser.add_argument('-p', '--past', nargs='?', const=0, type=int, default=0, required=True,
                        help="Use past # of days starting from 'date' as training data")
    args = parser.parse_args()

    past_days = args.past
    date = pd.to_datetime(str(args.date), format='%Y%m%d')
    future_days = args.future

    print(past_days, date, future_days)
    return future_days, date, past_days

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

def get_date_range(start_year, end_year, jump):
    start_date = datetime.date( year = start_year, month = 1, day = 1 )
    end_date = datetime.date( year = end_year, month = 12, day = 31 )
     
    dlist = []
    i = 0 
    if start_date <= end_date:
        for n in range( ( end_date - start_date ).days + 1 ):
            if i % jump == 0:
                dlist.append( start_date + datetime.timedelta( n ) )
            i = i + 1
    else:
        for n in range( ( start_date - end_date ).days + 1 ):
            if i % jump == 0:
                dlist.append( start_date - datetime.timedelta( n ) )
            i = i + 1

    date_to_str = lambda d: int(date_time_to_str(d))
    return list(map(date_to_str, dlist))

#if __name__ == "__main__":
def predict_oil_prices(future_days, past_days, date):
    # read from the command line
    # future_days, date, past_days = read_args()

    # countries_list = ["USA", "IND", "CHN", "EUU"]

    # STEP 1 - Read input CSVs

    houston_data = read_weather_data("houston_weather.csv")
    dhahran_data = read_weather_data("dhahran_weather.csv")
    omsk_data    = read_weather_data("omsk_weather.csv")
    AAL_data     = read_AAL_csv("AAL.csv") 
    WTI_data     = pd.read_csv("DCOILWTICO.csv")
    us_econ_data = get_economic_data()

    #gold_data1   = read_gold_data_csv("gold_current.csv")
    #gold_data2   = read_gold_data_csv("gold_previous.csv")
    #gold_data    = gold_data1.append(gold_data2)


    #create date range
    dates_list = get_date_range(2007, 2017, 1)
    dates_df = pd.DataFrame({'yyyymmdd':dates_list})

    # STEP 2 - merge CSV files

    # Merge the data for three cities and keep the union of the dates
    merged_weather = pd.merge(dates_df, houston_data, on='yyyymmdd', how='left')
    merged_weather = pd.merge(merged_weather, dhahran_data, on='yyyymmdd', how='left')
    merged_weather = pd.merge(merged_weather, omsk_data, on='yyyymmdd', how='left')
    #merged_weather = pd.merge(merged_weather, gold_data, on='yyyymmdd', how='left')
    merged_weather = pd.merge(merged_weather, AAL_data, on='yyyymmdd', how='left')
    #merged_weather = pd.merge(dates_df, us_econ_data, on='yyyymmdd', how='left')

    # STEP 3 - flatten the data based on past_days

    index_column = []
    count = 0
    for i in range(0, len(merged_weather)):
        if i % past_days == 0:
            count = count + 1
        index_column.append(count)

    merged_weather = merged_weather.assign(index=index_column)
    merged_weather = merged_weather.set_index(['index']).groupby(level=['index'])

    flat_merged = pd.DataFrame()
    for details, data in merged_weather:
        data_point = pd.concat([row for i, row in data.iterrows()]).to_frame()
        data_point.index = ['{}_{}'.format(label, i) for i, label in enumerate(data_point.index)]
        flat_merged = pd.concat([flat_merged, data_point], axis=1)
    flat_merged = flat_merged.transpose().reset_index()


    #with open('golddata.csv', 'w') as f:
    #    gold_data.to_csv(f, line_terminator='\n', index=False, header=True)
    with open('filelocation.csv', 'wb') as f:
        flat_merged.to_csv(f, line_terminator='\n', index=False, header=True)

    merged_weather = flat_merged

    # STEP 4 - format WTI prices to merge with the rest

    # Next step is to offset so you align how many days you wish to predict into the future with the present day!
    full_wti = pd.merge(dates_df, WTI_data, left_on='yyyymmdd', right_on='DATE', how='left')
    full_wti.DCOILWTICO = full_wti.DCOILWTICO.shift(-1*future_days)

    # Merge both dataframes and use only the dates which are available for both weather and WTI
    merged_data = pd.merge(merged_weather, full_wti, left_on='yyyymmdd_0', right_on='yyyymmdd', how='left')
    merged_data.drop(['DATE', 'yyyymmdd'], axis=1, inplace=True)
    date_cols_to_drop = []
    for i in range(1, len(merged_data.columns)):
        label_to_drop = 'yyyymmdd_{}'.format(i)
        if i > 0 and label_to_drop in merged_data.columns:
            date_cols_to_drop.append(label_to_drop)
    merged_data.drop(date_cols_to_drop, axis=1, inplace=True)
    # Replace NaN with mean
    merged_data.fillna(merged_data.mean()[:], inplace=True)
    merged_data = merged_data.round(2)
    merged_data = merged_data.stack().apply(pd.to_numeric, errors='ignore').fillna(0).unstack()
    merged_data.to_csv("merged_data.csv", sep=',')

    # STEP # - Split data to train and test data frames
    train_size = int(len(merged_data) * 0.8)
    test_size = len(merged_data) - train_size

    print("train_size = {} test_size = {}".format(train_size, test_size))

    train, test = merged_data[0:train_size], merged_data[train_size:]

    train_x, train_y = train.iloc[:,2:-1], train.iloc[:,-1]
    test_x, test_y = test.iloc[:,2:-1], test.iloc[:,-1]

    # STEP # - Trainig and testing
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(train_x, train_y)
    predicted = rf.predict(test_x)
    test.loc[:,'PredWTI'] = predicted

    # STEP # - Report results
    print("Mean Absolute Error:", mean_absolute_error(test_y, test['PredWTI']))
    print("Mean Squared Error:", mean_squared_error(test_y, test['PredWTI']))
    r2=r2_score(test_y.values, test['PredWTI'].values)
    print("R squared:", r2)
    test.loc[:,'diff'] = (1 - abs(test['DCOILWTICO'].values - test['PredWTI'].values)/test['DCOILWTICO'].values)
    avg = test['diff'].mean()
    print("Accuracy:", avg)

    test.sort_values(by=['yyyymmdd_0'], inplace=True)
    #test['DCOILWTICO'].plot(figsize=(16,12))
    #test['PredWTI'].plot(figsize=(16,12))
    #pl.show()

    return r2, avg, test
