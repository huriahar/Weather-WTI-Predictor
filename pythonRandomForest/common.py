import datetime

def date_time_to_str(d):
    d = str(d.year) + str(d.month).zfill(2) + str(d.day).zfill(2)
    return d

def get_date_range(start_date, end_date, jump):
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

