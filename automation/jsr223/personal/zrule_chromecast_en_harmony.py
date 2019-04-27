scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")

from core.log import logging
from core.triggers import ItemCommandTrigger, item_triggered, ITEM_UPDATE, ITEM_CHANGE, ITEM_COMMAND

class logitech_harmony_hub_toggle(SimpleRule):
    def __init__(self):
        self.triggers = [ItemCommandTrigger("logitech_harmony_hub_toggle", command="OFF") ]
    def execute(self, module, input):
        logging.info("Running rule_logitech_harmony_hub_toggle_off rule...")
        #if items.logitech_harmony_hub_toggle == OFF:
        events.sendCommand("logitech_harmony_hub_current_activity", "PowerOff")
        #else:
        #    pass
automationManager.addRule(logitech_harmony_hub_toggle())

@item_triggered("logitech_harmony_hub_current_activity",ITEM_CHANGE)
def rule_harmony_hub_initialize():
    logging.info("Running logitech_harmony_hub_current_activity hub rule...")
    if str(items.logitech_harmony_hub_current_activity) == "PowerOff":
        events.postUpdate("logitech_harmony_hub_toggle", "OFF")
    else:
        events.postUpdate("logitech_harmony_hub_toggle", "ON")

@item_triggered("logitech_harmony_hub_current_activity", ITEM_CHANGE)
def rule_logitech_harmony_hub_current_activity():
    logging.info("rule_logitech_harmony_hub_current_activity started....")

    if str(items.logitech_harmony_hub_current_activity) == "Listen to Spotify":
        if items.upc_horizon_box_harmony_hub != OFF: 	    		
            events.postUpdate("upc_horizon_box_harmony_hub", "OFF")
        if items.panasonic_tv_harmony_hub != OFF:
            events.postUpdate("panasonic_tv_harmony_hub", "OFF")
        if items.onkyo_receiver_harmony_hub != ON:			
            events.postUpdate("onkyo_receiver_harmony_hub", "ON")
	
        if items.logitech_harmony_hub_status != ON:  			
            events.postUpdate("logitech_harmony_hub_status","ON")
        if items.logitech_harmony_hub_toggle != ON:  			
            events.postUpdate("logitech_harmony_hub_toggle","ON")
    
    elif str(items.logitech_harmony_hub_current_activity) == "Video streamen":
        if items.upc_horizon_box_harmony_hub != OFF: 	    		
            events.postUpdate("upc_horizon_box_harmony_hub", "OFF")
        if items.panasonic_tv_harmony_hub != ON:				
            events.postUpdate("panasonic_tv_harmony_hub", "ON")
        if items.onkyo_receiver_harmony_hub != ON:			
            events.postUpdate("onkyo_receiver_harmony_hub", "ON")
	
        if items.logitech_harmony_hub_status != ON:  			
            events.postUpdate("logitech_harmony_hub_status","ON")
        if items.logitech_harmony_hub_toggle != ON:  			
            events.postUpdate("logitech_harmony_hub_toggle","ON")

    elif str(items.logitech_harmony_hub_current_activity) == "PowerOff":
        if items.upc_horizon_box_harmony_hub != OFF: 	    		
            events.postUpdate("upc_horizon_box_harmony_hub", "OFF")
        if items.panasonic_tv_harmony_hub != OFF:				
            events.postUpdate("panasonic_tv_harmony_hub", "OFF")
        if items.onkyo_receiver_harmony_hub != OFF:			
            events.postUpdate("onkyo_receiver_harmony_hub", "OFF")
	
        if items.logitech_harmony_hub_status !=OFF:  			
            events.postUpdate("logitech_harmony_hub_status","OFF")
        if items.logitech_harmony_hub_toggle != OFF:  		
            events.postUpdate("logitech_harmony_hub_toggle","OFF")

    elif str(items.logitech_harmony_hub_current_activity) == "Watch TV":
        if items.upc_horizon_box_harmony_hub != ON: 	    		
            events.postUpdate("upc_horizon_box_harmony_hub", "ON")
        if items.panasonic_tv_harmony_hub != ON:				
            events.postUpdate("panasonic_tv_harmony_hub", "ON")
        if items.onkyo_receiver_harmony_hub != ON:			
            events.postUpdate("onkyo_receiver_harmony_hub", "ON")
	
        if items.logitech_harmony_hub_status != ON:  			
            events.postUpdate("logitech_harmony_hub_status","ON")
        if items.logitech_harmony_hub_toggle != ON:  			
            events.postUpdate("logitech_harmony_hub_toggle","ON")


@item_triggered("logitech_harmony_hub_current_activity", ITEM_CHANGE)
def rule_chromecast_woonkamer_py_status_changed():
    if items.rule_chromecast_woonkamer_py_status_changed_is_running != ON and str(items.chromecast_woonkamer_py_status) != "BUFFERING":
        events.postUpdate("rule_chromecast_woonkamer_py_status_changed_is_running", "ON")
        # var boolean chromecast_is_active = (chromecast_woonkamer_py_status.state.toString == "PLAYING" || chromecast_woonkamer_py_status.state.toString == "PAUSED")// ||  chromecast_woonkamer_py_status.state.toString == "BUFFERING")

        if str(items.logitech_harmony_hub_current_activity) != "Listen to Spotify" and (str(items.chromecast_woonkamer_py_status) == "PLAYING" or str(items.chromecast_woonkamer_py_status) == "PAUSED") and str(items.chromecast_woonkamer_py_type) == "3":
 			 events.sendCommand("logitech_harmony_hub_current_activity", "Listen to Spotify")
	
        elif str(items.logitech_harmony_hub_current_activity) != "Video streamen" and (str(items.chromecast_woonkamer_py_status) == "PLAYING" or str(items.chromecast_woonkamer_py_status) == "PAUSED") and str(items.chromecast_woonkamer_py_type) != "3":
            events.sendCommand("logitech_harmony_hub_current_activity", "Video streamen")

        if str(items.logitech_harmony_hub_current_activity) == "Listen to Spotify" or str(items.logitech_harmony_hub_current_activity) == "Video streamen":
            
            if str(items.chromecast_woonkamer_py_status) == "PLAYING" or str(items.chromecast_woonkamer_py_status) == "PAUSED":
 				events.sendCommand("rule_chromecast_woonkamer_py_status_changed_start_harmony_poweroff", "ON")
            
            elif items.rule_chromecast_woonkamer_py_status_changed_start_harmony_poweroff == ON:
                events.sendCommand("rule_chromecast_woonkamer_py_status_changed_start_harmony_poweroff", "OFF")

 		events.postUpdate("rule_chromecast_woonkamer_py_status_changed_is_running", "OFF")



@item_triggered("rule_chromecast_woonkamer_py_status_changed_start_harmony_poweroff", ITEM_COMMAND) # deze rule moet naar een item toe.
def rule_turn_off_harmony_devices_delayed():
    if item.rule_chromecast_woonkamer_py_status_changed_start_harmony_poweroff == OFF:
        events.sendCommand("logitech_harmony_hub_current_activity", "PowerOff")