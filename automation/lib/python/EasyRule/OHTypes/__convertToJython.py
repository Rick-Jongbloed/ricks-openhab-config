from .. import OHImports
logger = OHImports.oh.getLogger("EasyRule.OHTypes.__convertToJython")


def ToNumeric(javaval, varname):
    if javaval is None:
        return None

    _str = str(javaval)
    try:
        return int(_str)
    except ValueError:
        try:
            return float(_str)
        except ValueError as e:
            logger.error("Error converting '{}' ({}) : {}!".format(varname, javaval, e))
            return None


def ToString(javaval, varname):
    if javaval is None:
        return None

    #use unicode for values!
    _str = unicode(javaval, "utf-8")

    if _str == u"Uninitialized":
        return None

    return _str



def ToTimestamp(javaval, varname):
    if javaval is None:
        return None

    _str = str(javaval)
    if _str == u"Uninitialized":
        return None

    try:
        return float( OHImports.DateTimeType( _str).calendar.timeInMillis ) / 1000.0
    except ValueError as e:
        logger.error("Error converting '{}' ({}) : {}!".format(varname, javaval, e))
        return None