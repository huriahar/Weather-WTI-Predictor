import pandas as pd
import numpy as np
import pylab as pl

from sklearn.ensemble import RandomForestRegressor
from sklearn.cross_validation import train_test_split
import pudb

from common import get_date_range
from read_input import read_weather_data
from read_input import read_AAL_csv
from read_input import get_economic_data

def predict_oil_prices(start_date, future_days, past_days, end_date):
    # STEP 1 - Read input CSVs

    houston_data = read_weather_data("houston_weather.csv")
    dhahran_data = read_weather_data("dhahran_weather.csv")
    omsk_data    = read_weather_data("omsk_weather.csv")
    AAL_data     = read_AAL_csv("AAL.csv") 
    WTI_data     = pd.read_csv("DCOILWTICO.csv")
    us_econ_data = get_economic_data()

    #create date range
    dates_list = get_date_range(start_date, end_date, 1)
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
    
    flat_merged = pd.DataFrame()
    for i in range(0, len(merged_weather)):
        data_point = pd.concat([row for j, row in merged_weather.iloc[i:i+past_days,:].iterrows()]).to_frame()
        data_point.index = ['{}_{}'.format(label, i) for i, label in enumerate(data_point.index)]
        flat_merged = pd.concat([flat_merged, data_point], axis=1)
    flat_merged = flat_merged.transpose()
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
    merged_data = merged_data.round(2)
    merged_data.fillna(method='ffill', inplace=True)

    #if a column is entirely empty, fill with zeros
    merged_data = merged_data.stack().apply(pd.to_numeric, errors='ignore').fillna(0).unstack()
    merged_data = merged_data.fillna(0)

    merged_data.to_csv("merged_data.csv", sep=',')

    # STEP # - Split data to train and test data frames

    train, test = merged_data[0:-1], merged_data[-2:-1]

    train_x, train_y = train.iloc[:,1:-2], train.iloc[:,-1]
    test_x, test_y = test.iloc[:,1:-2], test.iloc[:,-1]

    # STEP # - Trainig and testing
    rf = RandomForestRegressor(n_estimators=100)
    rf.fit(train_x, train_y)
    predicted = rf.predict(test_x)

    # STEP # - Report results
    return predicted[0], test_y.values[0]
