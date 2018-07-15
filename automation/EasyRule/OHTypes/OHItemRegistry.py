import org.openhab.core.items.ItemNotUniqueException
import org.openhab.core.items.ItemNotFoundException

import traceback

from ..OHImports import oh, ir
logger = oh.getLogger("EasyRule.OHTypes.OHItemRegistry")

from OHItem import ConvertItem

# ir.getItem(String itemName)
# ir.getItemByPattern(String name)
# ir.getItems()
# ir.getItems(String pattern)
# ir.isValidItemName(String itemName)

class ItemNotUniqueException(Exception):
    pass
class ItemNotFoundException(Exception):
    pass


def ItemExceptionHandler( func, p1):
    try:
        return func()
    except org.openhab.core.items.ItemNotUniqueException as e:
        logger.debug("{}".format(e))
        raise ItemNotUniqueException("Item cannot be uniquely identified by '{}'".format(p1))

    except org.openhab.core.items.ItemNotFoundException as e:
        logger.debug("{}".format(e))
        raise ItemNotFoundException("Item '{}' could not be found in the item registry".format(p1))


class OHItemRegistry():

    def __init__(self):
        self.ir = self.ItemRegistry = ir

    def getItem(self, itemName ):
        try:
            return ConvertItem(ir.getItem(itemName))
        except Exception as e:
            logger.error("{}\n{}".format(e, traceback.format_exc()))
            return None

    def getItemByPattern(self, pattern ):
        try:
            return ItemExceptionHandler( lambda : ConvertItem(ir.getItemByPattern(pattern)), pattern)
        except Exception as e:
            logger.error("{}\n{}".format(e, traceback.format_exc()))
            return None

    def getItems(self, pattern = None):
        items = None
        if pattern is None:
            items = ir.getItems()
        else:
            items = ir.getItems(pattern)

        for i in range(len(items)):
            items[i] = ConvertItem(items[i])
        return items

    def isValidItemName(self, itemName):
        return bool(ir.isValidItemName(itemName))

    def ItemExists(self, itemName):
        if not len(ir.getItems(itemName)):
            return False

        return True