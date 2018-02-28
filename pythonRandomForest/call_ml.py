import datetime
import os
import pylab as pl
from sklearn.metrics import r2_score

from infra_retrain import predict_oil_prices
from common import date_time_to_str
from common import get_date_range

######### DEFINE THE SOLUTION SPACE ############
MIN_YEAR = 2007
MAX_YEAR = 2017
################################################

def plot_params(predicted, actual):
    idx = [i for i in range(0, len(predicted))]
    pl.plot(idx, predicted, 'r')
    pl.plot(idx, actual, 'b')
    pl.show()

def testParams():
    fValues = [7]#[7, 14, 21]
    pValues = [4]#[21, 60, 30] 
    numTestPoints = 100
    trainingDays = 365
    max_day = datetime.date(year = MAX_YEAR, month = 12, day = 31)
    allPredicted = []
    allActual = []
    for f in fValues:
        for p in pValues:
            for t in range(0, numTestPoints):
                start_date = datetime.date( year = MIN_YEAR, month = 1, day = 1 )
                start_date = start_date + datetime.timedelta(days=(t))
                end_date = start_date + datetime.timedelta(days=(trainingDays + 1))
                test_date = end_date + datetime.timedelta(days=(f))
                if end_date > max_day: break;
                s = date_time_to_str(start_date)
                d = date_time_to_str(end_date)
                print "==================================================="
                print "Test point #{}".format(t)
                print "Start training on {}".format(s)
                print "End training on {}".format(d)
                print "Training days = {}".format(trainingDays)
                print "Future offset (f) = {} Past days per data point (p) = {}".format(f,p)
                print "Test day = {}".format(date_time_to_str(test_date))
                print "---------------------------------------------------"
                predicted, actual = predict_oil_prices(start_date, f, p, end_date)
                print "acutal = {}, predicted = {}".format(actual, predicted)
                allPredicted.append(predicted)
                allActual.append(actual)
    r2=r2_score(allActual, allPredicted)
    print "R2 = {}".format(r2)    
    acc = [1 if (abs(a-b)/a) < 0.03 else 0 for (a,b) in zip(allActual, allPredicted)]
    acc = sum(acc) / len(acc)
    print "Accuracy = {}".format(acc)    
    plot_params(allPredicted, allActual)

def main():
    testParams()

if __name__ == "__main__":
    main()


