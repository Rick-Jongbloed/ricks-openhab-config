import time

#openhab Imports
from EasyRule.openhab.log           import LOG_PREFIX, log_traceback
from EasyRule.openhab.jsr223        import scope, get_automation_manager, get_scope
from EasyRule.openhab.jsr223.scope  import SimpleRule

#Smarthome Magic
from org.eclipse.smarthome.automation import Rule as OpenhabRule
scope.scriptExtension.importPreset("RuleSimple")

import EasyRule._helper

#normal code
import logging, inspect, traceback
logger = logging.getLogger( LOG_PREFIX + ".EasyRule.rule")

from threading import Lock


def BaseRule_Decorator( cls):

    #set class Variables
    if not hasattr(cls, 'EasyRuleNames'):
        setattr(cls, 'EasyRuleNames', [])
    if not hasattr(cls, 'EasyRuleLock'):
        setattr(cls, 'EasyRuleLock', Lock())

    def __name_get(self):
        return self.__name
    def __name_set(self, val):
        try:
            cls.EasyRuleLock.acquire()

            if self.__name is not None:
                cls.EasyRuleNames.remove(self.__name)

            #create unique name
            i = 0
            used_name = val
            while used_name in cls.EasyRuleNames:
                i += 1
                used_name = '{:s}{:d}'.format(val, i)
            cls.EasyRuleNames.append(used_name)

            if isinstance(self, EasyRule.ScriptHelper):
                __uuid = '{:s}.{:s}'.format(cls.__name__, used_name)
            elif isinstance(self, FunctionDecoratorClass):
                __uuid = '{:s}.{:s}'.format(self.EasyRuleScriptHelper.name_helper, used_name)
            else:
                __uuid = '{:s}.{:s}.{:s}'.format(self.EasyRuleScriptHelper.name_helper, cls.__name__, used_name)


            self.UUID   = __uuid
            self.__name = used_name
            self.log    = logging.getLogger('{:s}.{:s}'.format(LOG_PREFIX, self.UUID))

            #set as UUID of Rule
            uid_field = type(OpenhabRule).getClass(OpenhabRule).getDeclaredField(OpenhabRule, "uid")
            uid_field.setAccessible(True)
            uid_field.set(self, __uuid)
        finally:
            cls.EasyRuleLock.release()

    def init(self, *args, **kwargs):
        SimpleRule.__init__(self)

        if not isinstance(self, EasyRule.ScriptHelper):
            self.EasyRuleScriptHelper = EasyRule._helper.GetScriptHelper()

        self.UUID   = None
        self.log    = None
        self.__name = None
        self.name = kwargs.pop("name", self.__class__.__name__)

        self.EasyRuleProperties   = { 'RunOnlyAfterInitialize' : True}
        self.EasyRuleValues       = { 'Initialized' : False, 'CheckedTriggers' : False, 'ExecutionCounter' : 0}

        __allowed_properties = self.EasyRuleProperties.keys()

        #make it possible to override stuff
        if getattr(cls, "__init__", None) is not None:
            cls.__init__( self, *args, **kwargs)

        assert isinstance(self.log, logging.Logger)

        #EasyRule-Properties which can be set through user
        assert isinstance(self.EasyRuleProperties, dict)
        assert isinstance(self.EasyRuleProperties['RunOnlyAfterInitialize'], bool)

        for k in self.EasyRuleProperties.keys():
            if not k in __allowed_properties:
                raise ValueError('Key "{}" not allowed in EasyRuleProperties!')


        #OH-Vars
        if self.description is None and cls.__doc__:
            self.description = cls.__doc__
        #Triggers
        try:
            if hasattr(self, "getEventTriggers"):
                self.triggers = self.getEventTriggers()
        except Exception as ex:
            tb = traceback.format_exc().splitlines()
            for line in tb:
                self.log.error(line)
            self.log.error('')
            raise

        #Required for the ScriptHelper, if we don't use this we get infinate loop
        if not isinstance(self, EasyRule.ScriptHelper):
            self.EasyRuleScriptHelper.AddRule(self)

        #finally add to Openhab
        get_automation_manager().addRule(self)
        return None

    #log error in case user forgets args
    nargs = len(inspect.getargspec(cls.execute).args)
    if nargs <= 2:
        logger.error("Error in class '{:s}': execute has to have at least 3 arguments! e.g.: 'def execute(self, module, input):'".format(cls.__name__))

    #Initialize-Function is important
    if not hasattr( cls, 'Initialize'):
        logger.warning('Rule "{:s}" has no "Initialize" function!'.format(cls.__name__))


    def repr(self):
        return "<Rule {:s}>".format(self.name)


    @log_traceback
    def execute( self, module, input):
        if self.EasyRuleProperties['RunOnlyAfterInitialize']:
            if self.EasyRuleValues['Initialized'] is False:
                return None

        start = time.time()
        cls.execute(self, module, EasyRule.replacements.event.ConvertRuleEventDict(input))
        self.EasyRuleValues['LastExecutionDuration'] = time.time() - start
        self.EasyRuleValues['ExecutionCounter'] += 1

    @log_traceback
    def initialize(self):
        if hasattr(cls, 'Initialize'):
            cls.Initialize(self)
        self.EasyRuleValues['Initialized'] = True


    override_dict = {'__init__': init, 'execute': execute, 'Initialize': initialize}
    if not hasattr(cls, "__repr__"):
        override_dict["__repr__"] = repr

    override_dict['name'] = property(fget= lambda self : self.__name_get(), fset= lambda self, value : self.__name_set(value))
    override_dict['__name_get'] = __name_get
    override_dict['__name_set'] = __name_set


    #replace init with newly defined one
    derived_class = type(cls.__name__, (cls, SimpleRule), override_dict)

    #what does this do?
    def new(cls, *args, **kwargs):
        return super(cls, cls).__new__(cls, *args, **kwargs)
    derived_class.__new__ = staticmethod(new)

    return derived_class



class FunctionDecoratorClass():
    def __init__(self, user_function, trigger, RunOnlyAfterInitialize=False):
        self.EasyRuleProperties['RunOnlyAfterInitialize'] = RunOnlyAfterInitialize
        self.func = user_function
        self.name = user_function.__name__
        self.triggers = [trigger]

    def execute(self, module, input):
        self.func(module, input)

    def Initialize(self):
        pass

def ItemChanged_Decorator( *args, **kwargs):
    _args = len(args)
    if _args != 3 and _args != 1:
        raise TypeError("ItemChanged requires 1 or 3 parameters! Given: {} [{}]".format(_args, args))

    def inner_func( user_function):
        trig = EasyRule.Triggers.ItemChanged( *args)
        BaseRule_Decorator(FunctionDecoratorClass)(user_function, trig, **kwargs)
    return inner_func

def ItemUpdated_Decorator( *args, **kwargs):
    _args = len(args)
    if _args != 1:
        raise TypeError("ItemUpdated requires 1 parameter! Given: {} [{}]".format(_args, args))

    def inner_func( user_function):
        trig = EasyRule.Triggers.ItemReceivedUpdate( *args)
        BaseRule_Decorator(FunctionDecoratorClass)(user_function, trig, **kwargs)
    return inner_func

def ItemCommand_Decorator( *args, **kwargs):
    _args = len(args)
    if _args != 1 and _args != 2:
        raise TypeError("ItemCommand requires 1 or 2 parameters! Given: {} [{}]".format(_args, args))

    def inner_func( user_function):
        trig = EasyRule.Triggers.ItemReceivedCommand( *args)
        BaseRule_Decorator(FunctionDecoratorClass)(user_function, trig, **kwargs)
    return inner_func

def Cron_Decorator( *args, **kwargs):
    _args = len(args)
    if _args != 1:
        raise TypeError("ItemUpdated requires 1 parameter! Given: {} [{}]".format(_args, args))

    def inner_func( user_function):
        trig = EasyRule.Triggers.CronTrigger( *args)
        BaseRule_Decorator(FunctionDecoratorClass)(user_function, trig, **kwargs)
    return inner_func