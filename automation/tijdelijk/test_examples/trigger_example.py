from core.triggers import ItemStateUpdateTrigger
from core.log import logging, LOG_PREFIX
scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")
class ItemStateUpdateTriggerExtension(SimpleRule):
    def __init__(self):
        self.triggers = [ItemStateUpdateTrigger("Test_Switch_1").trigger]
        self.name = "Jython Hello World (ItemStateUpdateTrigger extension)"
        self.description = "This is an example rule using an ItemStateUpdateTrigger extension"
        self.tags = set("Example rule tag")
        self.log = logging.getLogger("{}.Hello World (ItemStateUpdateTrigger extension)".format(LOG_PREFIX))
    def execute(self, module, inputs):
        self.log.info("Hello World!")
automationManager.addRule(ItemStateUpdateTriggerExtension())