
import datetime

#overridable weekday names
WEEKDAY_NAMES = {0 : "Mo", 1 : "Di", 2 : "Mi", 3 : "Do", 4 : "Fr", 5 : "Sa", 6 : "So"}

#List with public holidays, use datetime.MINYEAR for reoccuring entries
HOLIDAYS = [
    # New Year
    datetime.date(datetime.MINYEAR, 1, 1),

    # Labor Day
    datetime.date(datetime.MINYEAR, 5, 1),

    # German Unity
    datetime.date(datetime.MINYEAR, 3, 10),

    # All Hallows Day
    datetime.date(datetime.MINYEAR, 1, 11),

    #Christmas
    datetime.date(datetime.MINYEAR, 12, 24),
    datetime.date(datetime.MINYEAR, 12, 25),
    datetime.date(datetime.MINYEAR, 12, 26),
]

__today   = 0
__holiday = False

def is_holiday( date):
    global __today, __holiday

    assert isinstance(date, datetime.datetime)

    #cache, so we don't look up all the time
    if __today == date.date():
        return __holiday

    #new date
    __today = date.date()
    assert isinstance(__today, datetime.date), type(__today)


    for holiday in HOLIDAYS:
        #the user can change this -> better check
        assert isinstance(holiday, datetime.date), type(holiday)

        #reoccuring
        if holiday.year == datetime.MINYEAR:
            if holiday.month == __today.month and holiday.day == __today.day:
                __holiday = True
                break
        else:
            if __today == holiday:
                __holiday = True
                break

    return __holiday