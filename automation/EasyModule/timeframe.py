import datetime, re
from EasyModule.shared import WEEKDAY_NAMES, is_holiday

#function which generates the datetime obj
_TIME_FUNC = datetime.datetime.now


_RE_VALID = re.compile(r'^((?:\w+,)*)((?:\d+:\d+:?\d*)(?:-\d+:\d+:?\d*)?)$')
_RE_DAYS  = re.compile(r'(\w+),')
_RE_TIMES = re.compile(r'^(\d+:\d+:?\d*)(?:-(\d+:\d+:?\d*))?$')
_RE_TIME  = re.compile(r'^(\d+):(\d+)(?::(\d+))?$')

_DAYS = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}

for nr, day in WEEKDAY_NAMES.items():
    assert isinstance(nr, int),  '{}: {}'.format(type(nr), nr)
    assert isinstance(day, str), '{}: {}'.format(type(day), day)
    _DAYS[day.lower()] = nr


class TimeFrame(object):

    def __init__(self, timespan, sunday_checks_holiday = True, log_function = None):
        """
        Creates TimeFrame object.

        :param timespan: Description of time span. Omitting second time means untill end of day (23:59:59). E.g. "mon,8:30:00-9:31", "weekends,22:30:00", 'weekdays,8:30:00-9:30:00", "mon,tue,8:30:00-9:31:30"
        :param log_function: function for logging which takes 1 parameter
        """
        assert isinstance(timespan, str)
        if log_function is not None:
            assert callable(log_function)
        desc = timespan.lower().replace(' ', '')

        self.time_start = None # type: tuple
        self.time_stop  = None # type: tuple
        self.weekdays   = []   # type: list[int]

        self.__log_func = log_function

        m = _RE_VALID.search(desc)
        if not m or len(m.groups()) !=2:
            raise ValueError('Invalid format!')

        self.__get_days(m.group(1))
        self.__get_time(m.group(2))

        self.check_holidays = True if sunday_checks_holiday and 6 in self.weekdays else False

        self.__plausicheck_time()

        self.desc_weeks = ''
        for day in self.weekdays:
            self.desc_weeks += WEEKDAY_NAMES[day] + ","
        self.desc_time = '{:2d}:{:02d}:{:02d}-{:2d}:{:02d}:{:02d}'.format(self.time_start[0], self.time_start[1], self.time_start[2], \
                                                                           self.time_stop[0],  self.time_stop[1],  self.time_stop[2])

    def __plausicheck_time(self):
        ts = [self.time_start, self.time_stop]
        for t in ts:
            if not 0 <= t[0] <= 23:
                raise ValueError('Hour must be 0 - 23!')
            if not 0 <= t[1] <= 59 or not 0 <= t[2] <= 59:
                raise ValueError('Minutes and seconds must be 0 - 59!')

        t1 = self.time_start[0] * 3600 + self.time_start[1] * 60 + self.time_start[2]
        t2 = self.time_stop[0]  * 3600 + self.time_stop[1]  * 60 + self.time_stop[2]

        if t2 <= t1:
            raise ValueError('Stop must be after start!\nStart: {}\nStop : {}'.format(self.time_start, self.time_stop))

    def __get_days(self, desc):
        #no day is all days!
        if desc == "":
            for i in range(7):
                self.weekdays.append(i)
            return


        m = _RE_DAYS.findall(desc)
        if not m:
            raise ValueError('No day specified in "{}"'.format(desc))

        def add_day(x):
            if x not in self.weekdays:
                self.weekdays.append(x)

        for d in m:
            if d == 'weekdays':
                for i in range(5):
                    add_day(i)
            elif d == 'weekends':
                add_day(5)
                add_day(6)
            else:
                if d in _DAYS:
                    add_day(_DAYS[d])
                else:
                    raise ValueError('Value "{:s}" ist not a valid day! (Allowed: {})'.format(d, list(_DAYS.keys())))

    def __get_time(self, desc):
        m = _RE_TIMES.search(desc)
        assert len(m.groups()) == 2, m.groups()

        t1 = _RE_TIME.search(m.group(1))
        l1 = [ int(k) if k is not None else 0 for k in t1.groups()]

        #fehlt der zweite Eintrag dann gilt es bis Tagesende
        if m.group(2) is not None:
            t2 = _RE_TIME.search(m.group(2))
            l2 = [ int(k) if k is not None else 0 for k in t2.groups()]
        else:
            l2 = [23,59,59]

        assert len(l1) == 3, '{}'.format(l1)
        assert len(l2) == 3, '{}'.format(l2)

        self.time_start = tuple(l1)
        self.time_stop = tuple(l2)

    def __log(self, _in):
        if self.__log_func is not None:
            self.__log_func(_in)

    def is_now(self):
        """
        Compares the defined time span to now

        :return: True if now is in time span, else False
        """

        date_now = _TIME_FUNC()
        assert isinstance(date_now, datetime.datetime), type(date_now)

        self.__log('Def : {:s}{:s}'.format(self.desc_weeks, self.desc_time))
        __now_str = 'Now :{:>{width}s},{:2d}:{:02d}:{:02d}'.format(WEEKDAY_NAMES[date_now.weekday()], date_now.hour, date_now.minute, date_now.second, width= len(self.desc_weeks))

        day_now = date_now.weekday()


        if day_now not in self.weekdays and \
                not (self.check_holidays and is_holiday(date_now)):
            self.__log(__now_str + ' (False)')
            return False

        start = 3600 * self.time_start[0] + 60 * self.time_start[1] + self.time_start[2]
        stop  = 3600 * self.time_stop[0]  + 60 * self.time_stop[1]  + self.time_stop[2]
        now   = 3600 * date_now.hour      + 60 * date_now.minute    + date_now.second

        if start <= now <= stop:
            self.__log(__now_str + ' (True)')
            return True
        else:
            self.__log(__now_str + ' (False)')
            return False
