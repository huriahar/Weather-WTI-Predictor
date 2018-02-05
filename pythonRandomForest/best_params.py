import datetime
import os
from infra import predict_oil_prices
import pylab as pl

######### DEFINE THE SOLUTION SPACE ############
MIN_F = 1
MAX_F = 30
MAX_P = 1
MIN_P = 365
MIN_YEAR = 2007
MAX_YEAR = 2017
################################################

def get_date_range(start_year, end_year, jump):
    start_date = datetime.date( year = start_year, month = 1, day = 6 )
    end_date = datetime.date( year = end_year, month = 12, day = 30 )
     
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
    return dlist

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

def plot_params(params):
    lists = sorted(params.items()) # sorted by key, return a list of tuples
    datefp, acc = zip(*lists) # unpack a list of pairs into two tuples
    date, f, p = zip(*datefp)
    date = list(map(lambda d: datetime.datetime.strptime(d, '%Y%m%d'), date))
    #date = list(map(lambda d: int(d), date))
    pl.cla()
    pl.clf()
    pl.close()
    #f, p, acc = zip(*y)
    print date
    print acc
    #acc = list(acc)
    #pl.plot(date, acc, '^g')
    #pl.xlabel('date')
    #pl.ylabel('accuracy')
    #pl.ylim(-20, 10)

    fig, ax = pl.subplots()
    ax.scatter(date, acc)

    for idx, d in enumerate(date):
        pu.db
        ax.annotate('({},{},{})'.format(f[idx], p[idx], round(acc[idx],2)), (date[idx], acc[idx]), verticalalignment='bottom')
    pl.show()

def testParams():
    fValues = [7, 14, 21]
    pValues = [7, 21, 30] #, 270, 300, 365]
    yValues = [2009] #, 2012, 2013, 2014, 2015, 2016]
    max_rsquared = -99999999
    params = {}
    for f in fValues:
        for p in pValues:
            for y in yValues:
                dlist = get_date_range(y, y, 30)
                for d in dlist:
         	    date = str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2)
                    print "future = {} past = {} date = {}".format(f,p,date)
                    rsquared = call_ml(f, p, date)
                    params[(date, f, p)] = rsquared
                    if rsquared > max_rsquared:
                        max_rsquared = rsquared
                        max_params = (date, f, p)
    print "MAX rsquared = {} with params {}".format(max_rsquared, params[max_params])
    plot_params(params)

def main():
    testParams()

if __name__ == "__main__":
    main()


