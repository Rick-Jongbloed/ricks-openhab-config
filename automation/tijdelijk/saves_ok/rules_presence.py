scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from core.log import logging
from core.triggers import ItemCommandTrigger, when
from core.rules import rule

# Presence detection - 
# if presence is not detected, but was on, a timer is started (5m)
# if presence is detected, someone_is_present is set to ON
@rule("Set present timer when item g_present updates")
@when("Item g_present received update")
#@item_group_triggered("g_present", ITEM_UPDATE)
def rule_group_present_updated(event):
    #logging.info("Running present detection rule...")
    if items.g_present == ON and items.someone_is_present != ON:           # Someone came home, or an item is updated
        events.postUpdate("present_timer", "OFF")                          # Cancel the timer if necessary 
        events.sendCommand("someone_is_present", "ON")
    elif items.g_present == OFF and items.someone_is_present != OFF:        # Someone was home, but no activity is detected.
        events.sendCommand("present_timer", "ON")                           # start the timer, to turn someone_is_present off


class rule_present_timer_expired (SimpleRule):
    def __init__(self):
        self.triggers = [ ItemCommandTrigger("present_timer", command="OFF") ]
    def execute(self, module, input):
        logging.info("Running rule_present_timer_expired started... ")
        events.postUpdate("someone_is_present" , "OFF")
automationManager.addRule(rule_present_timer_expired())
