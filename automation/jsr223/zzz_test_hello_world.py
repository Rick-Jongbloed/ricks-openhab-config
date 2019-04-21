from org.slf4j import LoggerFactory

LoggerFactory.getLogger("org.eclipse.smarthome.automation.examples").info("Hello world, python is working!")

scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")

from openhab.jsr223.scope import items

#
# Add an attribute-resolver to the items map
#

def _item_getattr(self, name):
    return self[name]

type(items).__getattr__ = _item_getattr.__get__(items, type(items))

from openhab.log import logging
#from openhab.triggers import StartupTrigger
from lucid.triggers import StartupTrigger



from openhab.jsr223 import scope

class rule_test_error (SimpleRule):
    def __init__(self):
        self.triggers = [  StartupTrigger() ]
        #self.triggers = [  ItemStateChangeTrigger("test_switch") ]
    def execute(self, module, input):
        logging.info(input)
        logging.info("KRIJG NOU WAT ")
automationManager.addRule(rule_test_error())