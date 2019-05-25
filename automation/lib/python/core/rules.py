from inspect import isclass
from java.util import UUID

try:
    from org.openhab.core.automation import Rule as SmarthomeRule
except:
    from org.eclipse.smarthome.automation import Rule as SmarthomeRule

from core.log import logging, LOG_PREFIX, log_traceback
from core.jsr223 import scope, get_automation_manager

scope.scriptExtension.importPreset("RuleSimple")

# this needs some attention in order to work with Automation API changes in 2.4.0 snapshots since build 1319
def set_uid_prefix(rule, prefix=None):
    if prefix is None:
        prefix = type(rule).__name__
    uid_field = type(SmarthomeRule).getClass(SmarthomeRule).getDeclaredField(SmarthomeRule, "uid")
    uid_field.setAccessible(True)
    uid_field.set(rule, "{}-{}".format(prefix, str(UUID.randomUUID())))

class _FunctionRule(scope.SimpleRule):
    def __init__(self, callback, triggers, name=None, description=None, tags=None):
        self.triggers = triggers
        if name is None:
            if hasattr(callback, '__name__'):
                name = callback.__name__
            else:
                name = "JSR223-Jython"
        self.name = name
        callback.log = logging.getLogger(LOG_PREFIX + "." + name)
        self.callback = log_traceback(callback)
        if description is not None:
            self.description = description
        if tags is not None:
            self.tags = set(tags)
        
    def execute(self, module, inputs):
        try:
            self.callback(inputs.get('event'))
        except:
            import traceback
            self.callback.log.error(traceback.format_exc())

def rule(name=None, description=None, tags=None):
    def rule_decorator(object):
        if isclass(object):
            clazz = object
            def init(self, *args, **kwargs):
                scope.SimpleRule.__init__(self)
                if name is None:
                    if hasattr(clazz, '__name__'):
                        self.name = clazz.__name__
                    else:
                        self.name = "JSR223-Jython"
                else:
                    self.name = name
                #set_uid_prefix(self)
                self.log = logging.getLogger(LOG_PREFIX + "." + self.name)
                clazz.__init__(self, *args, **kwargs)
                if description is not None:
                    self.description = description
                elif self.description is None and clazz.__doc__:
                    self.description = clazz.__doc__
                if hasattr(self, "getEventTriggers"):
                    self.triggers = log_traceback(self.getEventTriggers)()
                if tags is not None:
                    self.tags = set(tags)
            subclass = type(clazz.__name__, (clazz, scope.SimpleRule), dict(__init__=init))
            subclass.execute = log_traceback(clazz.execute)
            new_rule = addRule(subclass())
            subclass.UID = new_rule.UID
            return subclass
        else:
            callable_obj = object
            simple_rule = _FunctionRule(callable_obj, callable_obj.triggers, name=name, description=description, tags=tags)
            new_rule = addRule(simple_rule)
            callable_obj.UID = new_rule.UID
            callable_obj.triggers = None
            return callable_obj
    return rule_decorator

def addRule(rule):
    logging.getLogger(LOG_PREFIX + ".core.rules").debug("Added rule [{}]".format(rule.name))
    return get_automation_manager().addRule(rule)
