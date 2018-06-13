from org.eclipse.smarthome.core.library.items import NumberItem     as _NumberItem
from org.eclipse.smarthome.core.library.items import StringItem     as _StringItem
from org.eclipse.smarthome.core.library.items import ContactItem    as _ContactItem
from org.eclipse.smarthome.core.library.items import DimmerItem     as _DimmerItem
from org.eclipse.smarthome.core.library.items import SwitchItem     as _SwitchItem
from org.eclipse.smarthome.core.library.items import DateTimeItem   as _DateTimeItem
from org.eclipse.smarthome.core.library.items import ColorItem      as _ColorItem
from org.eclipse.smarthome.core.library.items import LocationItem   as _LocationItem
from org.eclipse.smarthome.core.library.items import PlayerItem     as _PlayerItem
from org.eclipse.smarthome.core.items         import GroupItem      as _GroupItem


import EasyRule, logging
logger = logging.getLogger( EasyRule.LOG_PREFIX + ".EasyRule.Items")

from converters import convertOpenhabValue
from busevent   import BusEvent

import time, datetime

class _BaseItem(object):
    def __init__(self, oh_item):
        super(_BaseItem, self).__init__()

        self.type  = oh_item.type.encode('ascii')
        self.name  = oh_item.name.encode('ascii')
        self.label = unicode(oh_item.label)

        self.groupNames = tuple(k.encode('ascii') for k in oh_item.groupNames)

        #what is this?
        self.tags  = tuple(oh_item.tags)

        #save original item
        self.oh_item = oh_item

    @property
    def state(self):
        return convertOpenhabValue(self.oh_item.state)

    def postUpdate(self, value):
        BusEvent.postUpdate(self.name, value)

    def sendCommand(self, value):
        BusEvent.sendCommand(self.name, value)

    def dumpItem(self):
        logger = logging.getLogger("org.eclipse.smarthome.automation.rules.EasyRule")

        lines = []
        for k in range(5):
            lines.append([])

        def append(name):
            _type = getattr(self, name)
            _oh_type = getattr(self.oh_item, name)

            lines[0].append(name)
            lines[1].append(str(type(_type)))
            lines[2].append(str(_type))
            lines[3].append(str(type(_oh_type)))
            lines[4].append(str(_oh_type))

        append( 'type')
        append( 'name')
        append( 'label')
        append( 'state')
        append( 'tags')
        append( 'groupNames')

        width = [0 for k in range(4)]
        for k in range(4):
            for val in lines[k]:
                width[k] = max(width[k], len(val))

        #dump all
        logger.debug( "")
        logger.debug(
            '{:^{w0}s} | {:^{w1}s} : {:^{w2}s} | {:^{w3}s} : {:s}'.format('', 'New Type', 'Value', 'Oh Type', 'OH Value',
                                                                         w0=width[0], w1=width[1], w2=width[2],
                                                                         w3=width[3]))
        for line in range(len(lines[0])):
            logger.debug( '{:>{w0}s} | {:>{w1}s} : {:{w2}s} | {:>{w3}s} : {:s}'.format(lines[0][line], lines[1][line], lines[2][line], lines[3][line], lines[4][line],
                                                                                       w0=width[0], w1 = width[1], w2 = width[2], w3 = width[3]))

    # print("\n")
    # for k in dir(oh_item):
    #     if k[0:2] == '__':
    #         continue
    #     try:
    #         val = getattr(oh_item, k)
    #     except AttributeError as e:
    #         val = str(e)
    #     print( '{:30s} : {}'.format(k, val))

class StringItem(_BaseItem):
    def __init__(self, oh_item):
        super(StringItem, self).__init__(oh_item)

class NumberItem(_BaseItem):
    def __init__(self, oh_item):
        super(NumberItem, self).__init__(oh_item)

class ContactItem(_BaseItem):
    def __init__(self, oh_item):
        super(ContactItem, self).__init__(oh_item)

    @property
    def isClosed(self):
        return True if self.state == "CLOSED" else False

    @property
    def isOpen(self):
        return True if self.state == "OPEN" else False

class DimmerItem(_BaseItem):
    def __init__(self, oh_item):
        super(DimmerItem, self).__init__(oh_item)

class LocationItem(_BaseItem):
    def __init__(self, oh_item):
        super(LocationItem, self).__init__(oh_item)

class GroupItem(_BaseItem):
    def __init__(self, oh_item):
        super(GroupItem, self).__init__(oh_item)

class PlayerItem(_BaseItem):
    def __init__(self, oh_item):
        super(PlayerItem, self).__init__(oh_item)

class DateTimeItem(_BaseItem):
    def __init__(self, oh_item):
        super(DateTimeItem, self).__init__(oh_item)

    @staticmethod
    def __ConvertValue( value):
        if isinstance(value, float):
            value = time.localtime(value)

        if isinstance(value, time.struct_time):
            return time.strftime('%Y-%m-%dT%H:%M:%S.%f+%z')

        if isinstance(value, datetime.datetime) or \
           isinstance(value, datetime.date)     or \
           isinstance(value, datetime.time):
                # 2018-01-29T09:07:00.893+0100
                return value.strftime('%Y-%m-%dT%H:%M:%S.%f+%z')

        raise ValueError('Type {} not supported!'.format(type(value)))

    def postUpdate(self, value):
        BusEvent.postUpdate(self.name, DateTimeItem.__ConvertValue( value))

    def sendCommand(self, value):
        BusEvent.sendCommand(self.name, DateTimeItem.__ConvertValue( value))
    #datetime.strptime

class ColorItem(_BaseItem):
    def __init__(self, oh_item):
        super(ColorItem, self).__init__(oh_item)


class SwitchItem(_BaseItem):
    def __init__(self, oh_item):
        super(SwitchItem, self).__init__(oh_item)

    @property
    def isOn(self):
        return True if self.state == "ON" else False

    @property
    def isOff(self):
        return True if self.state == "Off" else False


def ConvertItem( ohitem):
    if ohitem is None:
        return None

    if isinstance(ohitem, _NumberItem):
        return NumberItem(ohitem)
    elif isinstance(ohitem, _StringItem):
        return StringItem(ohitem)
    elif isinstance(ohitem, _ContactItem):
        return ContactItem(ohitem)
    elif isinstance(ohitem, _DimmerItem):
        return DimmerItem(ohitem)
    elif isinstance(ohitem, _SwitchItem):
        return SwitchItem(ohitem)
    elif isinstance(ohitem, _DateTimeItem):
        return DateTimeItem(ohitem)
    elif isinstance(ohitem, _ColorItem):
        return ColorItem(ohitem)
    elif isinstance(ohitem, _LocationItem):
        return LocationItem(ohitem)
    elif isinstance(ohitem, _GroupItem):
        return GroupItem(ohitem)
    elif isinstance(ohitem, _PlayerItem):
        return PlayerItem(ohitem)

        # import inspect
    # for k in dir(ohitem.state):
    #     print("{:30} : {}".format(k, ""))

    raise ValueError( "Unknown item type \"{}\" : \"{}\"".format(type(ohitem), ohitem))