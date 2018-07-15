from ..OHImports import oh, BusEvent
logger = oh.getLogger("EasyRule.OHTypes.OHItemRegistry")


def do_conversion( val):
    if isinstance(val, str) or isinstance(val, unicode):
        return False
    return True

#primitive to String-Cast
class OHBusEvent():

    def sendCommand(self, itemName, val):

        if do_conversion(itemName):
            itemName = itemName.name
        if do_conversion(val):
            val = str(val)
        return BusEvent.sendCommand(itemName, val)

    def postUpdate(self, itemName, val):

        if do_conversion(itemName):
            itemName = itemName.name
        if do_conversion(val):
            val = str(val)
        return BusEvent.postUpdate(itemName, val)
