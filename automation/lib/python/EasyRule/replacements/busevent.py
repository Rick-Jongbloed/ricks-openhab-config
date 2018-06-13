from EasyRule.openhab.jsr223.scope import events

class BusEvent(object):

    @staticmethod
    def __cast_value(value):
        if isinstance(value, str):
            return value
        if isinstance(value, int) or isinstance(value, float):
            return str(value)
        raise ValueError('Type "{}" not supported!'.format(str(type(value))))


    @staticmethod
    def postUpdate( item, value):
        events.postUpdate(item, BusEvent.__cast_value(value))

    @staticmethod
    def sendCommand( item, value):
        events.sendCommand(item, BusEvent.__cast_value(value))
