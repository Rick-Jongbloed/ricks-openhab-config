scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from lucid.actions import Mqtt

from lucid.rules import rule, addRule
from lucid.triggers import ItemStateChangeTrigger, StartupTrigger, item_group_triggered, ITEM_UPDATE
from lucid.log import logging, LOG_PREFIX


# WORK IN PROGRESS BIJ DEZE RULE
@rule
class init_sonoff_maintenance_update_status_on_startup(object):

    def getEventTriggers(self):
        return [
            StartupTrigger() # Runs every startup
        ]


    def execute(self, module, input):
        function = 'sonoff.request_device_status'
        log = logging.getLogger(LOG_PREFIX + '.' + function)

        log.info("Rule init_sonoff_maintenance_update_status_on_startup started....")
        group = itemRegistry.getItem("g_maintenance_sonoff_action")
        for item in group.getAllMembers():
            if "__" in str(item.name):
                array = str(item.name).split("__")
                mqtt_device_name = str(array[1])

                log.info("Initializing MQTT item: '" + str(mqtt_device_name) + "' ...")

                Mqtt.publish("mosquitto", "cmnd/" + str(mqtt_device_name) + "/status", "0")
                Mqtt.publish("mosquitto", "cmnd/" + str(mqtt_device_name) + "/status", "2") # uitzoeken of dit nog nodig is
                Mqtt.publish("mosquitto", "cmnd/" + str(mqtt_device_name) + "/status", "11") # uitzoeken of dit nog nodig is
            else:
                log.info("MQTT TODO: ITEM:")
                log.info(item.name)

addRule(init_sonoff_maintenance_update_status_on_startup())

@item_group_triggered("g_sonoff_startup_states", ITEM_UPDATE)
def rule_g_sonoff_startup_states(event):
    function = 'sonoff.update_startup_state'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("Rule g_sonoff_startup_states started for item " + str(event.itemName))
    # for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
    item_name = str(event.itemName).replace("_startup_state", "")
    item_object = itemRegistry.getItem(item_name)
    if str(item_object.state) == "NULL":
        #logging.info("Item " + str(item_object.name) + " is NULL: " + str(item_object.state))
        events.postUpdate(item_name, str(event.itemState))
    else:
        pass

@item_group_triggered("g_sonoff_firmware", ITEM_UPDATE)
def rule_g_sonoff_firmware_report(event):
    function = 'sonoff.update_firmware_status'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("Rule_g_sonoff_firmware_report started for item " + str(event.itemName))
    #for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
    latest_firmware_item = itemRegistry.getItem("sonoff_current_firmware_version")
    item_name = str(event.itemName).replace("_local_fw_version", "_fw_version")
    
    if str(event.itemState) < str(latest_firmware_item.state):
        events.postUpdate(item_name, "Upgrade available from " + str(event.itemState) + " to " + str(latest_firmware_item.state))
    else:
        events.postUpdate(item_name, "Version " + str(event.itemState) + " is up to date")