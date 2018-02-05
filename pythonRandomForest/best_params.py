import datetime
import os

######### DEFINE THE SOLUTION SPACE ############
MIN_F = 1
MAX_F = 30
MAX_P = 1
MIN_P = 365
MIN_YEAR = 2007
MAX_YEAR = 2017
################################################

def get_date_range(start_year, end_year, jump):
    start_date = datetime.date( year = start_year, month = 1, day = 1 )
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
    os.system('python infra.py -f {} -p {} -d {}'.format(f, p, d))

def testParams():
    fValues = [7, 8, 9, 10]#, 14, 21, 30]
    pValues = [7, 8, 9, 10, 14] #, 7]#, 14, 21, 30, 60, 90, 120, 150, 180, 210, 270, 300, 365]
    yValues = [2009, 2010] #, 2011, 2012, 2013, 2014, 2015, 2016]
    for f in fValues:
        for p in pValues:
            for y in yValues:
                dlist = get_date_range(y, y, 1)
                for d in dlist:
         	    date = str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2)
                    print "future = {} past = {} date = {}".format(f,p,date)
                    call_ml(f, p, date)

def main():
    testParams()

if __name__ == "__main__":
    main()


