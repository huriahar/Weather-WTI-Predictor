import datetime
import os
import pylab as pl
from sklearn.metrics import r2_score

from infra_retrain import predict_oil_prices
from common import date_time_to_str
from common import get_date_range

######### DEFINE THE SOLUTION SPACE ############
MIN_YEAR = 2015
MAX_YEAR = 2017
###############################################

def plot_params(params, predicted, actual, r2, acc):
    idx = [i for i in range(0, len(predicted))]
    pl.figure(figsize=(25,10))
    pl.plot(idx, predicted, 'r', label = "Predicted", lw=7)
    pl.plot(idx, actual, 'b', label = "Actual", lw=7)
    pl.legend(loc = "upper right", shadow=True)
    pl.xlabel("Date", weight = "bold", size=30)
    pl.ylabel("WTI Crude Oil Price (USD)", weight = "bold", size=30)
    pl.title("Prediction using P = {}, F = {}, Y = {}".format(params[1], params[0], MIN_YEAR), weight = "bold", size = 40)
    pl.figtext(0.83, 0.5, "R-squared : {}\nAccuracy : {}".format(r2, acc), size=30)
    pl.subplots_adjust(left=0.05, right=0.8, top=0.9, bottom=0.1)
    pl.savefig("../Frontend/img/{},{},{}.png".format(params[1], params[0], MIN_YEAR), dpi = 100)
    # pl.show()

def testParams():
    pValues = [60]        # [5, 7, 14, 30, 60]
    fValues = [90]        # [1, 7, 14, 30, 60, 90]
    numTestPoints = 200
    trainingDays = 365
    max_day = datetime.date(year = MAX_YEAR, month = 12, day = 31)
    best_r2 = -999
    bestAccuracy = -99
    bestPredicted = []
    bestActual = []
    for f in fValues:
        for p in pValues:
            allPredicted = []
            allActual = []
            for t in range(0, numTestPoints):
                start_date = datetime.date( year = MIN_YEAR, month = 1, day = 1 )
                start_date = start_date + datetime.timedelta(days=(t))
                end_date = start_date + datetime.timedelta(days=(trainingDays))
                test_end_date = end_date + datetime.timedelta(days=(f))
                test_date = test_end_date + datetime.timedelta(days=(1-p))
                if end_date > max_day: break;
                s = date_time_to_str(start_date)
                d = date_time_to_str(end_date)
                print "==================================================="
                print "Test point #{}".format(t)
                print "Start training on_________: {}".format(s)
                print "End training on___________: {}".format(d)
                print "Test input begins on day__: {}".format(date_time_to_str(test_date))
                print "Test input ends on day____: {}".format(date_time_to_str(test_end_date))
                print "Today_____________________: {}".format(date_time_to_str(test_end_date))
                print "Training days = {}".format(trainingDays)
                print "Future offset (f) = {} Past days per data point (p) = {}".format(f,p)
                print "---------------------------------------------------"
                predicted, actual = predict_oil_prices(start_date, f, p, end_date, test_date)
                print "actual = {}, predicted = {}".format(actual, predicted)
                allPredicted.append(predicted)
                allActual.append(actual)
            r2=r2_score(allActual, allPredicted)
            print "R2 = {}".format(r2)    
            acc = [1 if (abs(a-b)/a) < 0.04 else 0 for (a,b) in zip(allActual, allPredicted)]
            acc = sum(acc)/float(len(acc))
            print "Accuracy = {}".format(acc)    
            if r2 > best_r2:
                best_r2 = r2
                bestPredicted = allPredicted
                bestActual = allActual
                bestAccuracy = acc
                bestParams = [f, p]
                
    print "==================================================="
    print "==================================================="
    print "==================================================="
    print "Best Parameters are: f = {} p = {}".format(bestParams[0], bestParams[1])
    print "r2 = {} Accuracy = {}".format(best_r2, bestAccuracy)
    plot_params(bestParams, bestPredicted, bestActual, round(best_r2,2), round(bestAccuracy,2))

def main():
    testParams()

if __name__ == "__main__":
    main()


