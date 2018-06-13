import functools

from OHImports import ChangedEventTrigger, UpdatedEventTrigger, TimerTrigger, CommandEventTrigger
from OHImports import StringType, DecimalType
from OHImports import oh
logger = oh.getLogger("EasyRule.SimpleRules")

import BaseRule
import __helper




@BaseRule.BaseRuleDecorator
class SimpleRule():
    def __init__(self, trigger, function, *args, **kwargs):
        self.__trig = trigger
        self.__func = function

    def getEventTrigger(self):
        return [ self.__trig ]

    def execute(self, event):
        self.__func(event)

    def Initialize(self):
        pass







def __MapDataTypes( _in):
    if type(_in) is str:
        return StringType(_in)

    if type(_in) is int:
        return DecimalType(_in)

    return _in

def __MapUpserFunction(user_function):
    _arg_count = user_function.__code__.co_argcount
    _name = user_function.__name__
    logger.debug("User Function '{}' has {} args".format(_name, _arg_count))
    # print(user_function.__code__.co_varnames)  # var name of args
    # print(user_function.__defaults__)  # arg with defaults --> https://docs.python.org/3/library/inspect.html#inspect.Parameter

    #throw away event - item if it is not defined
    if _arg_count == 0:
        return lambda x : user_function()
    return user_function



def CommandDecorator( *args):
    _args = len(args)
    logger.debug("Call CommandDecorator with {} args: {}".format(_args, args))
    if _args != 2 and _args != 1:
        logger.error("CommandDecorator requires 1 or 2 parameters! Given: {} [{}]".format(_args, args))
        return None

    def inner_func( user_function):
        trig = None
        if _args == 1:
            trig = CommandEventTrigger( str(args[0]) )
        else:
            trig = CommandEventTrigger( str(args[0]) , __MapDataTypes(args[1]))

        SimpleRule( trig, __MapUpserFunction(user_function), name=user_function.__name__)

    return inner_func



def ItemChangedDecorator( *args):
    _args = len(args)
    logger.debug("Call ItemChangedDecorator with {} args: {}".format(_args, args))
    if _args != 3 and _args != 1:
        logger.error("ItemChangedDecorator requires 1 or 3 parameters! Given: {} [{}]".format(_args, args))
        return None

    def inner_func( user_function):
        trig = None
        if _args == 1:
            trig = ChangedEventTrigger( str(args[0]) )
        else:
            trig = ChangedEventTrigger( str(args[0]) , __MapDataTypes(args[1]), __MapDataTypes(args[2]))

        assert trig is not None
        SimpleRule( trig, __MapUpserFunction(user_function), name=user_function.__name__)

    return inner_func

def ItemUpdatedDecorator( *args):
    _args = len(args)
    logger.debug("Call ItemUpdatedDecorator with {} args: {}".format(_args, args))
    if _args != 1:
        logger.error("ItemUpdatedDecorator requires 1 parameter! Given: {} [{}]".format(_args, args))
        return None

    def inner_func( user_function):
        SimpleRule( UpdatedEventTrigger( str(args[0])), __MapUpserFunction(user_function), name=user_function.__name__)

    return inner_func


def TimerTriggerDecorator( *args):
    _args = len(args)
    logger.debug("Call TimerTriggerDecorator with {} args: {}".format(_args, args))
    if _args != 1:
        logger.error("TimerTriggerDecorator requires 1 parameter! Given: {} [{}]".format( _args, args))
        return None

    def inner_func( user_function):
        SimpleRule( TimerTrigger( str(args[0])), __MapUpserFunction(user_function), name=user_function.__name__)

    return inner_func