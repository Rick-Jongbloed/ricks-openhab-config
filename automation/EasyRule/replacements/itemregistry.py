import org.eclipse.smarthome.core.items.ItemNotUniqueException
import org.eclipse.smarthome.core.items.ItemNotFoundException

import re

import EasyRule
import EasyRule.replacements
ir = EasyRule.openhab.jsr223.scope.ir

#import logging
#_logger = logging.getLogger( EasyRule.LOG_PREFIX + ".EasyRule.ItemRegistry")


class ItemNotUniqueException(Exception):
    pass
class ItemNotFoundException(Exception):
    pass


def _ItemExceptionHandler( fn):
    def wrapper(p1):
        try:
            return fn(p1)
        except org.eclipse.smarthome.core.items.ItemNotUniqueException as e:
            #_logger.debug("{}".format(e))
            raise ItemNotUniqueException("Item cannot be uniquely identified by '{}'".format(p1))

        except org.eclipse.smarthome.core.items.ItemNotFoundException as e:
            #_logger.debug("{}".format(e))
            raise ItemNotFoundException("Item '{}' could not be found in the item registry".format(p1))
    return wrapper


_CustomItems = {}

class ItemRegistry(object):

    @staticmethod
    def AddCustomItem( name, item):
        #check that we do not redefinition items
        if name in _CustomItems and type(item) is not type(_CustomItems[name]):
            raise TypeError( 'Redifinition of item "{:s}" from {:s} to {:s}'.format(name, type(item), type(_CustomItems[name])))
        _CustomItems[name] = item

    @staticmethod
    def RemoveCustomItem( name):
        if not name in _CustomItems:
            raise LookupError('No custom item with the name "{:s}" found!'.format(name))
        return _CustomItems.pop(name)


    @staticmethod
    def __find_custom_items( pattern):
        if pattern is None:
            return _CustomItems.values()

        ret = []
        r = re.compile(pattern)
        for k, v in _CustomItems.items():
            if r.search(k):
                ret.append(v)
        return ret

    @staticmethod
    def getItem( itemName , search_custom_items = True):
        if search_custom_items and itemName in _CustomItems:
            return _CustomItems[itemName]
        return EasyRule.replacements.items.ConvertItem( _ItemExceptionHandler(ir.getItem)(itemName))

    @staticmethod
    def getItemByPattern( pattern ):
        return EasyRule.replacements.items.ConvertItem(_ItemExceptionHandler(ir.getItemByPattern)(pattern))

    @staticmethod
    def getItems( pattern = None):
        ret = ItemRegistry.__find_custom_items(pattern)
        _items = ir.getItems() if pattern is None else ir.getItems(pattern)

        for i in range(len(_items)):
            ret.append( EasyRule.replacements.items.ConvertItem(_items[i]))
        return ret

    @staticmethod
    def ItemExists( itemName):
        try:
            _item = ItemRegistry.getItem(itemName)
        except ItemNotFoundException:
            return False
        return True
