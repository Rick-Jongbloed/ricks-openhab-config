from core.log import logging, LOG_PREFIX
from core.rules import rule
from core.triggers import when
from core.osgi import get_service

scriptExtension.importPreset("RuleSupport")

## USED TO BE A STARTUP TRIGGER
# NOW ITS A CRON JOB WHICH DISABLES ITSELF
@rule("Initialize sonoff devices - request status")
@when("Time cron 0/10 * * * * ?")
def init_sonoff_maintenance_update_status_on_startup(event):
    function = 'sonoff.request_device_status'
    log = logging.getLogger(LOG_PREFIX + '.' + function)


    log.info("@@@@@@@@@@@@@@@@@@@@ Rule init_sonoff_maintenance_update_status_on_startup started....")
    group = itemRegistry.getItem("g_maintenance_sonoff_action")
    for item in group.getAllMembers():
        if "__" in str(item.name):
            array = str(item.name).split("__")
            mqtt_device_name = str(array[1])

            log.info("Initializing MQTT item: '" + str(mqtt_device_name) + "' ...")
            actions.get("mqtt", "mqtt:broker:local").publishMQTT("cmnd/" + str(mqtt_device_name) + "/status", "0")
        else:
            log.info("MQTT TODO: ITEM:")
            log.info(item.name)
    # Now disable the rule 
    ruleUID = filter(lambda rule: rule.name == "Initialize sonoff devices - request status", rules.getAll())[0].UID
    ruleEngine = get_service("org.eclipse.smarthome.automation.RuleManager")
    ruleEngine.setEnabled(ruleUID, False) # disable rule


@rule("Process sonoff startup states")
@when("Item g_sonoff_startup_states received update")
def rule_g_sonoff_startup_states(event):
    function = 'sonoff.update_startup_state'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("@@@@@@@@@@@@@@@@@@@@ Rule g_sonoff_startup_states started for item " + str(event.itemName) + "' which updated to value '" + str(event.itemState) + "'")
    # for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
    item_name = str(event.itemName).replace("_startup_state", "")
    item_object = itemRegistry.getItem(item_name)
    if str(item_object.state) == "NULL":
        logging.info("Item " + str(item_object.name) + " is NULL: " + str(item_object.state))
        events.postUpdate(item_name, str(event.itemState))


@rule("Set firmware items with text value")
@when("Member of g_sonoff_firmware received update")
def rule_g_sonoff_firmware_report(event):
    function = 'sonoff.update_firmware_status'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("@@@@@@@@@@@@@@@@@@@@ Rule_g_sonoff_firmware_report started for item " + str(event.itemName))
    #for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
    latest_firmware_item = itemRegistry.getItem("sonoff_current_firmware_version")
    item_name = str(event.itemName).replace("_local_fw_version", "_fw_version")
    
    if str(event.itemState) < str(latest_firmware_item.state):
        events.postUpdate(item_name, "Upgrade available from " + str(event.itemState) + " to " + str(latest_firmware_item.state))
    else:
        events.postUpdate(item_name, "Version " + str(event.itemState) + " is up to date")
