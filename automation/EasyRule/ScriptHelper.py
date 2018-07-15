import EasyRule.rule
import EasyRule.Triggers
import EasyRule.replacements.itemregistry

import os

@EasyRule.rule.BaseRule_Decorator
class ScriptHelper():
    InitializationItem = "Initialize"

    def __SetScriptPath(self, path):
        if not path.startswith("file:/"):
            self.log.error( 'Path not supported: "{}"'.format(path))
            return
        self.script_path = os.path.abspath(path[6:])
        self.log.debug( 'Path: "{:s}"'.format(self.script_path))

        #Make __file__ Available
        self.script_vars['__file__'] = os.path.basename(self.script_path)

    @EasyRule.log_traceback
    def scriptLoaded(self, *args):
        if len(args):
            self.__SetScriptPath(args[0])
        for func in self.script_loaded_funcs:
            func(self.script_vars, self.script_automation_manager, *args)

    @EasyRule.log_traceback
    def scriptUnloaded(self):
        for func in self.script_unloaded_funcs:
            func(self.script_vars, self.script_automation_manager)

    def __init__(self, helper_name, script_vars = None, automation_manager = None, *args, **kwargs):
        self.name_helper = helper_name
        self.name = helper_name
        self.path = ""

        self.script_automation_manager = None
        self.script_path  = None
        self.script_vars = script_vars
        self.script_loaded_funcs   = []
        self.script_unloaded_funcs = []


        #self.name = "ScriptHelper." + helper_name

        #Sonst wird .execute nie aufgerufen
        self.EasyRuleProperties["RunOnlyAfterInitialize"] = False

        # init vars
        self.__rules = []
        self.__rules.append(self)

        #trigger so check gets done
        self.triggers = [EasyRule.Triggers.StartupTrigger(), # name='Startup_' + helper_name),
                         EasyRule.Triggers.ItemChanged(ScriptHelper.InitializationItem, state="ON")]

        self.item_exists = False
        #self.initialized = {}
        #self.rule_checked = {}

    @EasyRule.log_traceback
    def execute(self, module, input):

        if not self.item_exists:
            self.item_exists = EasyRule.ItemRegistry.ItemExists(ScriptHelper.InitializationItem)
        if not self.item_exists:
            return None

        for rule in self.__rules:
            if rule != self:
                self.ValidateRuleTriggers(rule)
        #self.log.debug('ScriptHelper.execute -> Initialize')
        for rule in self.__rules:
            if rule != self:
                rule.Initialize()

    @EasyRule.log_traceback
    def AddRule(self, obj):
        self.__rules.append(obj)
        self.log.debug( 'Added {:s} : {:s}'.format( obj.name, type(obj)))

        if not self.item_exists:
            return None

        self.ValidateRuleTriggers(obj)

        if self.EasyRuleValues["Initialized"] is True:
            obj.Initialize()

    @EasyRule.log_traceback
    def ValidateRuleTriggers(self, rule):

        if rule.EasyRuleValues['CheckedTriggers'] is True:
            return None

        self.log.info('+{:s}'.format('-' * 80))
        self.log.info('| Checking Triggers of Rule {}:'.format(rule.name))

        _triggers = rule.triggers
        assert isinstance(_triggers, list)

        for trigger in _triggers:
            conf_keys = trigger.configuration.keySet()
            if 'itemName' in conf_keys:
                item = trigger.configuration.get('itemName')
                if not EasyRule.ItemRegistry.ItemExists(item):
                    self.log.error('| - Item "{:s}" does not exist (Error)!'.format(item))
                else:
                    self.log.info('| - Item "{:s}" does exists (OK)!'.format(item))

        self.log.info('+{:s}'.format('-' * 80))
        rule.EasyRuleValues['CheckedTriggers'] = True
        #a.configuration.get('itemName')

        #self.initialized[obj.name] = False
        #self.rule_checked[obj.name] = False

        # if not self.item_exists:
        #     self.item_exists = EasyRule.ItemRegistry.ItemExists(ScriptHelper.InitializationItem)

        # if self.item_exists:
        #     self.log.debug('Initializing "{:s}"'.format(obj.name))
        #     obj.Initialize()
        #     self.initialized[obj.name] = True

    #should get never called
    def Initialize(self):
        pass

    def GetRules(self):
        return self.__rules

    def __repr__(self):
        __list = self.__rules
        if __list and __list[0] == self:
            __list[0] = "self"
        __list = str(__list).replace("'self'", "self")
        return '<ScriptHelper \'{}\': {}>'.format(self.name, __list)