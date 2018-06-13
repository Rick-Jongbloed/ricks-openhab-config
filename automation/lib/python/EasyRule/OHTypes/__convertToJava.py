from .. import OHImports
logger = OHImports.oh.getLogger("EasyRule.OHTypes.__convertToJava")


def FromString(val, varname):
    if isinstance(val, str):
        return val
    return str(val)