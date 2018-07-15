from ..OHImports import BusEvent, oh, HSBType
logger = oh.getLogger("EasyRule.OHTypes.OHItem")

from __convertToJython  import ToString,    ToNumeric, ToTimestamp
from __convertToJava    import FromString

class BaseItem:

    def __init__(self, ohitem):

        self.type = self.__class__.__name__
        self.reprstr = ""

        assert ohitem is not None
        self.ohitem = ohitem
        self.name   = str(ohitem.name)

    #refresh value directly from item
    #I am not sure if this can update alone?
    @property
    def state(self):
        return self.convertValueToJython(self.ohitem.state)


    def convertValueToJython(self, val):
        return ToString(val, self.name)

    def convertValueToJava(self, val):
        return FromString( val, self.name)

    def __repr__(self):
        return u"{} (Type={}, State={}, {}ohitem=(...))".format( self.name, self.type, self.state, self.reprstr + ", " if self.reprstr != "" else "")

    def postUpdate(self, new_state):
        BusEvent.postUpdate( self.ohitem, self.convertValueToJava(new_state))

    def sendCommand(self, command):
        BusEvent.postUpdate( self.ohitem, self.convertValueToJava(command))


class ContactItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

        self.isOpen   = True if self.state == "OPEN"   else False
        self.isClosed = True if self.state == "CLOSED" else False
        self.reprstr = "isOpen={}, isClosed={}".format( str(self.isOpen), str(self.isClosed))

class SwitchItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

        self.isOn  = True if self.state == "ON"  else False
        self.isOff = True if self.state == "OFF" else False
        self.reprstr = "isOn={}, isOff={}".format( str(self.isOn), str(self.isOff))

class StringItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

class NumberItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

    def convertValueToJython(self, val):
        return ToNumeric(val, self.name)


class PercentItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

    def convertValueToJython(self, val):
        return ToNumeric(val, self.name)

class DimmerItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

    def convertValueToJython(self, val):
        return ToNumeric(val, self.name)

class DateTimeItem(BaseItem):
    def __init__(self, ohitem):
        BaseItem.__init__(self, ohitem)

    def convertValueToJython(self, val):
        return ToTimestamp(val, self.name)


class ColorItem(BaseItem):
    def __init__(self, ohitem):
        self.hue        = None
        self.saturation = None
        self.brightness = None

        #deklaration unbedingt vorher, hier werden sie gesetzt!
        BaseItem.__init__(self, ohitem)
        self.reprstr = "hue={}, saturation={}, brightness={}".format(self.hue, self.saturation,self.brightness)

    def convertValueToJython(self, val):
        state = ToString(val, self.name)
        if state is None:
            return

        #update values
        hsb = HSBType(state)
        self.hue        = ToNumeric(hsb.hue,        self.name + ".hue")
        self.saturation = ToNumeric(hsb.saturation, self.name + ".saturation")
        self.brightness = ToNumeric(hsb.brightness, self.name + ".brightness")
        return state



def ConvertItem( ohitem):
    if ohitem is None:
        return None

    _type = str(type(ohitem))

    if _type == "<type 'org.openhab.core.library.items.NumberItem'>":
        return NumberItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.StringItem'>":
        return StringItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.PercentItem'>":
        return PercentItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.ContactItem'>":
        return ContactItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.DimmerItem'>":
        return DimmerItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.SwitchItem'>":
        return SwitchItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.DateTimeItem'>":
        return DateTimeItem(ohitem)
    elif _type == "<type 'org.openhab.core.library.items.ColorItem'>":
        return ColorItem(ohitem)

    # import inspect
    # for k in dir(ohitem.state):
    #     print("{:30} : {}".format(k, ""))

    logger.warn( "Unknown item type \"{}\" : \"{}\"".format(_type, ohitem))
    return BaseItem(ohitem)




