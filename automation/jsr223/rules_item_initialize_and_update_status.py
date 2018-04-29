scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
from openhab.triggers import time_triggered, item_triggered, StartupTrigger, ItemCommandTrigger, EVERY_MINUTE, ITEM_CHANGE, item_group_triggered
# from datetime import datetime
# from java.util import Date


class rule_startup_initialize(SimpleRule):
    def __init__(self):
        self.triggers = [ StartupTrigger() ]
    def execute(self, module, input):
        logging.info("Rule rule_startup_initialize: started....")

        logging.info("Rule rule_startup_initialize: Triggering Chromecast data initialization.....")  
        events.sendCommand("chromecast_woonkamer_py_update", "ON")
        
        logging.info("Rule rule_startup_initialize: Setting presence to OFF.....")  
        events.sendCommand("someone_is_present", "OFF")

        logging.info("Rule rule_startup_initialize: Initializing group g_uninitialized: Removing all items.....")   
        group = itemRegistry.getItem("g_uninitialized")
        for item in group.getAllMembers():
            group.removeMember(item)

        logging.info("Rule rule_startup_initialize: Initializing group g_uninitialized: Adding all items: Starting timer (120 secs)....")   
        events.sendCommand("rule_uninitialized_items_add_start", "ON")
        
        # logging.info("Rule rule_startup_initialize: Initializing computer on/off buttons: Mediacenter PC....")   
        # events.postUpdate("mediacenter_pc_turn_on", "OFF")
        # events.postUpdate("mediacenter_pc_turn_off", "OFF")

        logging.info("Rule rule_startup_initialize: Initializing computer on/off buttons: Office PC....")   
        events.postUpdate("kantoor_pc_turn_on", "OFF")
        events.postUpdate("kantoor_pc_turn_off", "OFF")

        logging.info("Rule rule_startup_initialize: Initializing computer on/off buttons: Spacecave PC....")   
        events.postUpdate("spacecave_pc_turn_on", "OFF")
        events.postUpdate("spacecave_pc_turn_off", "OFF")

        logging.info("Rule rule_startup_initialize: Initializing All unknown all off setting items (if there are any)....")
        group = itemRegistry.getItem("settings_all_off_selection")
        for item_setting in group.getAllMembers():
            if str(item_setting.state) == "NULL":
                logging.info("*** Initializing setting item: '" + item_setting.name + "' (to ON)")
                events.postUpdate(item_setting.name, "ON")

        # not really needed, because item is initialized while the timer
        logging.info("Rule rule_startup_initialize: Initializing all off timer....")
        events.postUpdate("rule_xiaomi_switch_kantoor_all_off_timer", "OFF")
automationManager.addRule(rule_startup_initialize())

@time_triggered(EVERY_MINUTE)
def rule_manage_group_unitialized_items():
    if items.rule_uninitialized_items_add_start == OFF:                 #Timer is turned off (after 120 secs past startup)
        #logging.info("Running uninitialize maintenance task: removing initialized items...")
        written_logging_line = False
        group = itemRegistry.getItem("g_uninitialized")
        for item in group.getAllMembers():
            if str(item.state) != "NULL":
                if written_logging_line == False:
                    logging.info("Running uninitialize maintenance task: removing initialized items...")
                written_logging_line = True
                logging.info("*** Removing item: " + item.name)
                group.removeMember(item)


class rule_uninitialized_items_add_items (SimpleRule):
    def __init__(self):
        self.triggers = [ ItemCommandTrigger("rule_uninitialized_items_add_start", command="OFF") ]
    def execute(self, module, input):
        logging.info("Running uninitialize maintenance task: timer expired, adding uninitialized items...")
        group_initialize = itemRegistry.getItem("g_uninitialized")
        group_devices = itemRegistry.getItem("devices")
        for item_device in group_devices.getAllMembers():
            if str(item_device.state) == "NULL":
                logging.info("*** Adding item: " + item_device.name)
                group_initialize.addMember(item_device)
automationManager.addRule(rule_uninitialized_items_add_items())


@item_group_triggered("g_lastupdate_rule")
def rule_g_lastupdate_rule(event):
    logging.info("Running rule_g_lastupdate_rule for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
    item_name = str(event.itemName) + "_lastupdate"
    events.postUpdate(item_name, str(DateTimeType()))
    
