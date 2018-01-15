import pandas as pd
import re, argparse
import pylab as pl
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

# Read file
# TODO: Add CSV file extension checks
def read_weather_data (file_name):    
    df = pd.read_csv(file_name, na_values=['-'])
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

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--future', nargs='?', const=0, type=int,
                    help="Add the number of days from the given day that you wish to make the prediction for")
parser.add_argument('-d', '--date', nargs='?', const=0, type=int,
                    help="Enter date in format yyyymmdd. Starting from this date..predict")
parser.add_argument('-p', '--past', nargs='?', const=0, type=int,
                    help="Use past # of days starting from 'date' as training data")
args = parser.parse_args()

# TODO: Add error checks for each of the inputs supplied
future_days = 0 if args.future is None else args.future
date = 0 if args.date is None else pd.to_datetime(str(args.date), format='%Y%m%d')
past_days = 0 if args.past is None else args.past
print(past_days, date, future_days)

houston_data = read_weather_data("houston_weather.csv")
dhahran_data = read_weather_data("dhahran_weather.csv")
omsk_data    = read_weather_data("omsk_weather.csv")

# Merge the data for three cities and keep the union of the dates
merged_weather = pd.merge(houston_data, dhahran_data, on='yyyymmdd', how='outer')
merged_weather = pd.merge(merged_weather, omsk_data, on='yyyymmdd', how='outer')
# print(merged_weather.columns)
# print(merged_weather.mean())
# merged_weather.to_csv('merged_weather.csv')
# print(merged_weather.isna().sum())

# Dhahran's temperature, pressure, humidity has 36 NaNs
# Replace NaN with mean
merged_weather.fillna(merged_weather.mean()['houston_temperature':'omsk_precipitation'], inplace=True)
# print(merged_weather.isna().sum())

# merged_weather = pd.read_csv("merged_weather.csv")

WTI_data = pd.read_csv("DCOILWTICO.csv")
# print(WTI_data.isna().sum())

# Merge both dataframes and use only the dates which are available for both weather and WTI
# TODO: Find a better way of merging both dataframes and keeping only one column out of DATE or yyyymmdd
merged_data = pd.merge(merged_weather, WTI_data, left_on='yyyymmdd', right_on='DATE', how='inner')
# print(merged_data.isna().sum())
merged_data.drop(['DATE'], axis=1, inplace=True)

merged_data['Date'] = merged_data['yyyymmdd'].apply(lambda x: pd.to_datetime(str(x), format='%Y%m%d'))
merged_data.set_index('Date', inplace=True)
# merged_data['DCOILWTICO'].plot(figsize=(16,12))

# merged_data.to_csv('merged_data.csv')

# Next step is to offset so you align how many days you wish to predict into the future with the present day!
merged_data.DCOILWTICO = merged_data.DCOILWTICO.shift(-1*future_days)
# Last future_days rows contain NaN for DCOILWTICO...
# TODO: Figure out what to do with that - Just ignore when splitting train and test

# Now, if date is supplied, start prediction from the given date. If not, use default separator at 80% of total data
# If past is supplied, use only the past number of days before given date for training. If not, use all the data before the "date"

# TODO: Add edge case checks!!! Now just assuming that if both date and past is supplied, you have plenty of training data available
# This will break if you supply random values! Check!!!
if date in merged_data.index:
    print(merged_data.loc[date, :])
    print("Location idx:", merged_data.index.get_loc(date))
    start_test_idx = merged_data.index.get_loc(date)
else:
    start_test_idx = int((len(merged_data) - future_days)*0.8)

# TODO: Add error checks for past # being out of bounds
if past_days != 0 and (start_test_idx - past_days) >= 0:
    start_train_idx = start_test_idx - past_days
else:
    start_train_idx = 0

print(start_train_idx, start_test_idx)
# Time Series split of train and test data 80-20

train, test = merged_data[start_train_idx:start_test_idx], merged_data[start_test_idx:(len(merged_data)-future_days)]
print("Total observations: %d" % (len(merged_data) - future_days))
print("Training observations: %d" % len(train))
print("Testing observations: %d" % len(test))

train_x, train_y = train.iloc[:,1:-1], train.iloc[:, -1]
test_x, test_y = test.iloc[:,1:-1], test.iloc[:, -1]

rf = RandomForestRegressor(n_estimators=50)

rf.fit(train_x, train_y)
test['PredWTI'] = rf.predict(test_x)

print("Mean Absolute Error:", mean_absolute_error(test_y, test['PredWTI']))
print("Mean Squared Error:", mean_squared_error(test_y, test['PredWTI']))
r2=r2_score(test_y, test['PredWTI'])
print("R squared:", r2)

test['DCOILWTICO'].plot(figsize=(16,12))
test['PredWTI'].plot(figsize=(16,12))
