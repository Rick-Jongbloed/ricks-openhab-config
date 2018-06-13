from org.eclipse.smarthome.core.library.types   import StringType, DecimalType, OnOffType, DateTimeType
from org.eclipse.smarthome.core.types           import UnDefType

from java.util import Calendar
import datetime

# Workaround for Jython JSR223 bug where
# dates and datetimes are converted to java.sql.Date
# and java.sql.Timestamp
def remove_java_converter(clazz):
    if hasattr(clazz, '__java__'):
        del clazz.__java__
    if hasattr(clazz, '__tojava__'):
        del clazz.__tojava__
remove_java_converter(datetime.date)
remove_java_converter(datetime.datetime)


def convertOpenhabValue(value):

    # #Don't convert native types
    # if value is None or \
    #         isinstance(value, bool) or isinstance(value, str) or \
    #         isinstance(value, int)  or isinstance(value, float) or isinstance(value, unicode):
    #     return value

    if isinstance(value, UnDefType):
        return None

    if isinstance(value, StringType):
        u = unicode(value)
        try:
            return u.encode('ascii')
        except UnicodeEncodeError:
            return u

    if isinstance(value, OnOffType):
        return str(value)

    if isinstance(value, DateTimeType):
        cal = value.calendar
        return datetime.datetime(
            cal.get(Calendar.YEAR),
            cal.get(Calendar.MONTH) + 1,
            cal.get(Calendar.DAY_OF_MONTH),
            cal.get(Calendar.HOUR_OF_DAY),
            cal.get(Calendar.MINUTE),
            cal.get(Calendar.SECOND),
            cal.get(Calendar.MILLISECOND) * 1000,
        )


    if isinstance(value, DecimalType):
        _str = value.toString()
        try:
            return int(_str)
        except ValueError:
            try:
                return float(_str)
            except ValueError as e:
                raise "Error converting '{}' ({}) : {}!".format(value, e)
                return None

    raise ValueError('No converter for {}'.format(type(value)))