import datetime
import os
import pylab as pl
from infra import date_time_to_str
from infra import predict_oil_prices
from infra import get_date_range

######### DEFINE THE SOLUTION SPACE ############
MIN_F = 1
MAX_F = 30
MAX_P = 1
MIN_P = 365
MIN_YEAR = 2007
MAX_YEAR = 2017
################################################

# def linear_search(args):
#     dlist = get_date_range()	 
#     for f in range(MIN_F, MAX_F):
# 	for p in range(MIN_P, MAX_P):
# 	    for d in dlist:
# 		date = str(d.year) + str(d.month) + str(d.day)
# 		call_ml(f, p, date)
# 
#def valid_date(s):
#    try:
#        return datetime.strptime(s, "%Y-%m-%d")
#    except ValueError:
#        msg = "Not a valid date: '{0}'.".format(s)
#        raise argparse.ArgumentTypeError(msg)
# return s.replace('-','')

def call_ml(f, p, d):
    print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    print('Future = {}, past = {} and start date is {}'.format(f, p, d))
    #os.system('python infra.py -f {} -p {} -d {}'.format(f, p, d))
    return predict_oil_prices(f, p, d)

def plot_params(params, test):
    lists = sorted(params.items()) # sorted by key, return a list of tuples
    datefp, acc = zip(*lists) # unpack a list of pairs into two tuples
    date, f, p = zip(*datefp)
    date = list(map(lambda d: datetime.datetime.strptime(d, '%Y%m%d'), date))
    #date = list(map(lambda d: int(d), date))
    pl.cla()
    pl.clf()
    pl.close()
    #f, p, acc = zip(*y)
    #acc = list(acc)
    #pl.plot(date, acc, '^g')
    #pl.xlabel('date')
    #pl.ylabel('accuracy')
    #pl.ylim(-20, 10)

    fig, ax = pl.subplots()
    ax.scatter(date, acc)

    for idx, d in enumerate(date):
        ax.annotate('({},{},{})'.format(f[idx], p[idx], round(acc[idx],2)), (date[idx], acc[idx]), verticalalignment='bottom')
    pl.show()
    pl.cla()
    pl.clf()
    pl.close()
    test['DCOILWTICO'].plot(figsize=(16,12), color='b')
    test['PredWTI'].plot(figsize=(16,12), color='g')
    pl.show()

def testParams():
    fValues = [7, 14, 21]
    pValues = [7, 21, 30] #, 270, 300, 365]
    max_rsquared = -99999999
    max_avg = 0
    params = {}
    for f in fValues:
        for p in pValues:
            start_date = datetime.date( year = MIN_YEAR, month = 1, day = 1 )
            date = start_date + datetime.timedelta(days=(p+1))
            d = date_time_to_str(date)
            print "future = {} past = {} date = {}".format(f,p,d)
            rsquared, avg, results = call_ml(f, p, d)
            params[(d, f, p)] = rsquared
            if rsquared > max_rsquared:
                max_rsquared = rsquared
                max_params = (d, f, p)
                max_results = results
                max_avg = avg
    print "MAX rsquared = {} accuracy = {} with params {}".format(max_rsquared, max_avg, max_params)
    plot_params(params, results)

def main():
    testParams()

if __name__ == "__main__":
    main()


