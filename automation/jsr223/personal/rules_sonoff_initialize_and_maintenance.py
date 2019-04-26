# Migrated to Lucid

# scriptExtension.importPreset("RuleSimple")
# scriptExtension.importPreset("RuleSupport")

#from openhab.triggers import ItemStateChangeTrigger, StartupTrigger, item_group_triggered, ITEM_UPDATE
# from openhab.triggers import ItemStateChangeTrigger, item_group_triggered, ITEM_UPDATE
# from lucid.triggers import StartupTrigger
# from openhab.log import logging
# from openhab.actions import Mqtt


# @item_group_triggered("g_sonoff_startup_states", ITEM_UPDATE)
# def rule_g_sonoff_startup_states(event):
#     logging.info("Rule g_sonoff_startup_states started for item " + str(event.itemName))
#     # for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
#     item_name = str(event.itemName).replace("_startup_state", "")
#     item_object = itemRegistry.getItem(item_name)
#     if str(item_object.state) == "NULL":
#         #logging.info("Item " + str(item_object.name) + " is NULL: " + str(item_object.state))
#         events.postUpdate(item_name, str(event.itemState))
#     else:
#         pass


# @item_group_triggered("g_sonoff_firmware", ITEM_UPDATE)
# def rule_g_sonoff_firmware_report(event):
#     logging.info("Rule_g_sonoff_firmware_report started for item " + str(event.itemName))
#     #for '" + event.itemName + "' which updated to value '" + str(event.itemState) + "'")
#     latest_firmware_item = itemRegistry.getItem("sonoff_current_firmware_version")
#     item_name = str(event.itemName).replace("_local_fw_version", "_fw_version")
    
#     if str(event.itemState) < str(latest_firmware_item.state):
#         events.postUpdate(item_name, "Upgrade available from " + str(event.itemState) + " to " + str(latest_firmware_item.state))
#     else:
#         events.postUpdate(item_name, "Version " + str(event.itemState) + " is up to date")


# already disabled
# @item_triggered("switch_sonoff_maintenance_action", ITEM_COMMAND)
# def rule_sonoff_action_received_command():
#     logging.info("Rule Sonoff maintenance on all devices started")
#     group = itemRegistry.getItem("g_maintenance_sonoff_action")
#     for item in group.getAllMembers():
#         if recieve
            
# goal 1: manage firmware init

# 	logInfo("sonoff.rules", "Sonoff Maintenance on all devices: " + receivedCommand)
# 	//logInfo("sonoff.rules", "Sonoff Maintenance on all devices: " + sonoff_device_ids.state.toString )
	
#     g_maintenance_sonoff_action?.members.forEach(device_id | 
# 		switch (receivedCommand) {
#             case "restart" :
#                 publish("broker", "cmnd/" + device_id + "/restart", "1") 
#             case "query_fw" :
#                 publish("broker", "cmnd/" + device_id + "/status", "2")
#             case "upgrade" : {
# 				publish("broker", "cmnd/" + device_id + "/otaurl", "http://sonoff.maddox.co.uk/tasmota/sonoff.bin")
#                 publish("broker", "cmnd/" + device_id + "/upgrade", "1")
# 				logInfo("sonoff.rules", "Sonoff Maintenance on device: '"+ device_id + "' command: '" + receivedCommand + "' executed")    
#             }
#         }
#     )
#     switch_sonoff_maintenance_action.postUpdate(NULL)
# end



