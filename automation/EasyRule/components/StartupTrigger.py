from org.eclipse.smarthome.automation import Visibility
from org.eclipse.smarthome.automation.handler import TriggerHandler
from org.eclipse.smarthome.automation.type import TriggerType

import EasyRule.openhab
EasyRule.openhab.STARTUP_MODULE_ID = "jsr223.StartupTrigger"

def scriptLoaded(scope, automation_manager, *args):
    #scope.scriptExtension.importPreset("RuleSupport")
    #scope.scriptExtension.importPreset("RuleFactories")

    class _StartupTriggerHandlerFactory(automation_manager.TriggerHandlerFactory):
        class Handler(TriggerHandler):
            def __init__(self, trigger):
                self.trigger = trigger

            def setRuleEngineCallback(self, rule_engine_callback):
                rule_engine_callback.triggered(self.trigger, {'startup': True})

            def dispose(self):
                pass

        def get(self, trigger):
            return _StartupTriggerHandlerFactory.Handler(trigger)

        def ungetHandler(self, module, ruleUID, handler):
            pass

        def dispose(self):
            pass

    automation_manager.addTriggerHandler(
        EasyRule.openhab.STARTUP_MODULE_ID,
        _StartupTriggerHandlerFactory())

    automation_manager.addTriggerType(TriggerType(
        EasyRule.openhab.STARTUP_MODULE_ID, [],
        "the rule is activated", 
        "Triggers when a rule is activated the first time",
        set(), Visibility.VISIBLE, []))

def scriptUnloaded(scope, automation_manager):
    automation_manager.removeHandler(EasyRule.openhab.STARTUP_MODULE_ID)
    automation_manager.removeModuleType(EasyRule.openhab.STARTUP_MODULE_ID)
