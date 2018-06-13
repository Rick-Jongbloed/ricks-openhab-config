from converters import convertOpenhabValue

from org.eclipse.smarthome.core.items.events import ItemCommandEvent        as _ItemCommandEvent
from org.eclipse.smarthome.core.items.events import ItemStateChangedEvent   as _ItemStateChangedEvent
from org.eclipse.smarthome.core.items.events import ItemStateEvent          as _ItemStateEvent


class ItemBaseEvent(object):
    def __init__(self, event):
        self.type     = event.type.encode('ascii')
        self.itemName = event.itemName.encode('ascii')

        # what is this stuff?? :S
        self.topic   = event.topic.encode('ascii')
        self.payload = unicode(event.payload)  # json-encoded values of class? Why?
        self.source  = None if event.source is None else event.source.encode('ascii')

    def __repr__(self):
        # without format specifiers because it can be anything
        return "<ItemBaseEvent type:'{}' itemName:'{}' source:'{}' payload:'{}' >".format(
            self.type, self.itemName, self.source, self.payload)

class ItemUpdatedEvent(ItemBaseEvent):
    def __init__(self, event):
        assert isinstance(event, _ItemStateChangedEvent), "{}".format(type(event))

        ItemBaseEvent.__init__(self, event)
        self.itemState = convertOpenhabValue(event.itemState)

    def __repr__(self):
        # without format specifiers because it can be anything
        return "<ItemUpdatedEvent type:'{}' itemName:'{}' itemState:'{}' source:'{}' payload:'{}' >".format(
            self.type, self.itemName, self.itemState, self.source, self.payload)

class ItemChangedEvent(ItemBaseEvent):
    def __init__(self, event):
        assert isinstance(event, _ItemStateChangedEvent), "{}".format(type(event))
        ItemBaseEvent.__init__(self, event)

        self.itemState    = convertOpenhabValue(event.itemState)
        self.oldItemState = convertOpenhabValue(event.oldItemState)

    def __repr__(self):
        #without format specifiers because it can be anything
        return "<ItemChangedEvent type:'{}' itemName:'{}' oldItemState:'{}' itemState:'{}' source:'{}' payload:'{}' >".format(self.type, self.itemName, self.oldItemState, self.itemState, self.source, self.payload)

class ItemCommandEvent(ItemBaseEvent):
    def __init__(self, event):
        assert isinstance(event, _ItemCommandEvent), "{}".format(type(event))
        ItemBaseEvent.__init__(self, event)

        self.itemCommand = convertOpenhabValue(event.itemCommand)

    def __repr__(self):
        #without format specifiers because it can be anything
        return "<ItemCommandEvent type:'{}' itemName:'{}' itemCommand:'{}' source:'{}' payload:'{}' >".format(self.type, self.itemName, self.itemCommand, self.source, self.payload)


def ConvertRuleEventDict( in_dict):

    ret = {}
    for key, value in in_dict.items():
        key = key.encode('ascii')
        if key == "module":
            ret[key] = value.encode('ascii')
        else:
            #ret[key] = value
            #continue
            #print('{:30s} : {} : {}'.format(key, type(value), value))
            if isinstance(value, _ItemStateChangedEvent):
                ret[key] = ItemChangedEvent(value)
            elif isinstance(value, _ItemStateEvent):
                ret[key] = ItemUpdatedEvent(value)
            elif isinstance(value, _ItemCommandEvent):
                ret[key] = ItemCommandEvent(value)
            #StartUp-Trigger has bool as value
            elif isinstance(value, bool):
                ret[key] = value
            else:
                ret[key] = convertOpenhabValue(value)
    return ret