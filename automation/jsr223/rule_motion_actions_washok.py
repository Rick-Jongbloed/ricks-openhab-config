scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
from openhab.triggers import ItemStateUpdateTrigger, ItemCommandTrigger, StartupTrigger
from openhab.actions import Mqtt, Pushover

class rule_motion_wasmachine_light (SimpleRule):
    def __init__(self): #itemName, state=None, triggerName=None
        self.triggers = [ 
                            StartupTrigger(),
                            ItemStateUpdateTrigger("sensor_motion_wasmachine_motion_status", state="ON"),
                            ItemStateUpdateTrigger("switch_licht_wasmachine_button_toggle"),
                            ItemCommandTrigger("timer_rule_motion_wasmachine_light_detected_motion", command="OFF"),
                            ItemCommandTrigger("timer_rule_motion_wasmachine_light_manual_off", command="OFF"),
                            ItemCommandTrigger("timer_rule_motion_wasmachine_light_init_hardware", command="OFF")
                        ]

    def execute(self, module, input):
        # logging.info(input)
        # logging.info("timer_rule_motion_wasmachine_light_detected_motion: " + str(items.timer_rule_motion_wasmachine_light_detected_motion))
        # logging.info("sensor_motion_wasmachine_motion_status: " + str(items.sensor_motion_wasmachine_motion_status))
        # logging.info("switch_licht_wasmachine_toggle: " + str(items.switch_licht_wasmachine_toggle))
        # logging.info("switch_licht_wasmachine_led_power: " + str(items.switch_licht_wasmachine_led_power))
        # logging.info("switch_licht_wasmachine_led_state: " + str(items.switch_licht_wasmachine_led_state))
        # logging.info("switch_licht_wasmachine_button_topic: " + str(items.switch_licht_wasmachine_button_topic))
        # logging.info("switch_licht_wasmachine_button_toggle: " + str(items.switch_licht_wasmachine_button_toggle))
        # logging.info("timer_rule_motion_wasmachine_light_manual_off: " + str(items.timer_rule_motion_wasmachine_light_manual_off))
        # logging.info("*************************************************************")

        # initialize programmable items
        if str(items.timer_rule_motion_wasmachine_light_detected_motion) == "NULL":
            events.postUpdate("timer_rule_motion_wasmachine_light_detected_motion","OFF") 
        
        if str(items.timer_rule_motion_wasmachine_light_manual_off) == "NULL":
            events.postUpdate("timer_rule_motion_wasmachine_light_manual_off","OFF") 
        
        #initialize non-pollable items
        if str(items.sensor_motion_wasmachine_motion_status) == "NULL":
            events.postUpdate("sensor_motion_wasmachine_motion_status","OFF")

        # initialize button (so it doesn't show in the un init list)
        if str(items.switch_licht_wasmachine_button_toggle) == "NULL":
            events.postUpdate("switch_licht_wasmachine_button_toggle","UNSET")
        
        #initialize pollable items
        if str(items.switch_licht_wasmachine_toggle) == "NULL" or str(items.switch_licht_wasmachine_led_power) == "NULL" or str(items.switch_licht_wasmachine_button_topic) != "sonoff_licht_washoek_button" or str(items.switch_licht_wasmachine_led_state) == "NULL":
            # initialize relay state item
            if str(items.switch_licht_wasmachine_toggle) == "NULL" or str(items.switch_licht_wasmachine_led_state) == "NULL":
                if str(items.switch_licht_wasmachine_toggle) == "NULL":
                    logging.info("Switch lamp washoek is in unknown state, pending refresh")
                if str(items.switch_licht_wasmachine_led_state) == "NULL":
                    logging.info("Led state of switch washoek is in unknown state, pending refresh")
                
                #Mqtt.publish("mosquitto", "cmnd/" + "sonoff_licht_washoek" + "/status", "0")

            # initialize led power item by querying led state (0=OFF, 8=ON)
            if str(items.switch_licht_wasmachine_led_power) == "NULL":
                logging.info("Led power van lamp washoek is in unknown state, pending refresh")
                if str(items.switch_licht_wasmachine_led_state) == "0":
                    events.postUpdate("switch_licht_wasmachine_led_power","OFF")
                    logging.info("POSTUPDATING  LED POWER TO OFF")
                elif str(items.switch_licht_wasmachine_led_state) == "8":
                    logging.info("POSTUPDATING  LED POWER TO ON")
                    events.postUpdate("switch_licht_wasmachine_led_power","ON")
                else:
                    logging.info("UNKNOWN LED STATE. UNABLE TO SET LEDPOWER (state: " + str(items.switch_licht_wasmachine_led_state))
               
            # initialize button topic (set button topic to 'sonoff_licht_washoek_button')
            if str(items.switch_licht_wasmachine_button_topic) != "sonoff_licht_washoek_button":
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_licht_washoek/ButtonTopic", "sonoff_licht_washoek_button")

            # Reschedule in 30 seconds until the items are in a proper state, if timer is somehow not yet running
            if items.timer_rule_motion_wasmachine_light_init_hardware != ON:
                logging.info("Setting refresh timer (30s) & updateting MQTT Status")
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_licht_washoek" + "/status", "0")
                events.sendCommand("timer_rule_motion_wasmachine_light_init_hardware","ON")        
            else:
                logging.info("Not scheduling inittimer because it is already set (<30s): " + str(items.timer_rule_motion_wasmachine_light_init_hardware))
            
            logging.info("timer_rule_motion_wasmachine_light_detected_motion: " + str(items.timer_rule_motion_wasmachine_light_detected_motion))
            logging.info("sensor_motion_wasmachine_motion_status: " + str(items.sensor_motion_wasmachine_motion_status))
            logging.info("switch_licht_wasmachine_toggle: " + str(items.switch_licht_wasmachine_toggle))
            logging.info("switch_licht_wasmachine_led_power: " + str(items.switch_licht_wasmachine_led_power))
            logging.info("switch_licht_wasmachine_led_state: " + str(items.switch_licht_wasmachine_led_state))
            logging.info("switch_licht_wasmachine_button_topic: " + str(items.switch_licht_wasmachine_button_topic))
            logging.info("switch_licht_wasmachine_button_toggle: " + str(items.switch_licht_wasmachine_button_toggle))
            logging.info("timer_rule_motion_wasmachine_light_manual_off: " + str(items.timer_rule_motion_wasmachine_light_manual_off))
            logging.info("*************************************************************")
        else:
            # start of procedure
            if "event" in input:
                trigger = str(input['event'])
               
            else:
                trigger = "startup"
             
            # logging.info(trigger)
            if "sensor_motion_wasmachine_motion_status" in trigger:
                # motion detected
                if items.switch_licht_wasmachine_led_power == OFF:
                    logging.info("motion detected and automatic mode is ON. (Re)setting timer and keeping light on for 5 minutes")
                    
                    #only setting light to on when it's not on yet. Otherwise only reset the timer.
                    if items.switch_licht_wasmachine_toggle == OFF:
                        events.sendCommand("switch_licht_wasmachine_toggle", "ON")
                    events.sendCommand("timer_rule_motion_wasmachine_light_detected_motion", "ON")
                else:
                    logging.info("motion detected and automatic mode is OFF (override is ON")
                    # do nothing
            
            elif "switch_licht_wasmachine_button_toggle" in trigger:
                # logging.info("Button press detected...")
                if items.switch_licht_wasmachine_led_power == OFF:
                    # zet led state & manual override aan (verplaats de MQTT publish /detect naar een aparte rule/class)
                    events.sendCommand("switch_licht_wasmachine_led_power","ON")

                    # forcing ledstate update to make it detectable on openhab/rule restart
                    Mqtt.publish("mosquitto", "cmnd/" + "sonoff_licht_washoek" + "/status", "")
                    
                    # manual mode, zet timer uit als deze aan staat
                    if items.timer_rule_motion_wasmachine_light_detected_motion == ON:
                        events.postUpdate("timer_rule_motion_wasmachine_light_detected_motion", "OFF")
                    
                    # zet licht aan als het op dit moment uit staat
                    if items.switch_licht_wasmachine_toggle == OFF:
                        events.sendCommand("switch_licht_wasmachine_toggle", "ON")
                    else:
                        # doe niks als het licht op dit moment aan staat
                        pass
                else:
                    # zet manual override uit?
                    if items.switch_licht_wasmachine_toggle == ON:
                        events.sendCommand("switch_licht_wasmachine_toggle", "OFF")
                        events.sendCommand("timer_rule_motion_wasmachine_light_manual_off", "ON")
                    else:
                        # zet het licht aan als de override aan staat en toggle is uit. Laat led power aan.
                        events.sendCommand("switch_licht_wasmachine_toggle", "ON")

            elif "timer_rule_motion_wasmachine_light_manual_off" in trigger:
                # state can only be OFF in this trigger
                # logging.info("Setting manual override & led_power to off, indicating that automatic mode is ON")
                events.sendCommand("switch_licht_wasmachine_led_power","OFF")
                
                # forcing ledstate update to make it detectable on openhab/rule restart
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_licht_washoek" + "/status", "")

            elif "timer_rule_motion_wasmachine_light_detected_motion" in trigger:
                # state can only OFF in this trigger
                # logging.info("Timer expired, turning off light")
                events.sendCommand("switch_licht_wasmachine_toggle", "OFF")
                # ergens moet deze timer gecancelled worden, overal waar manual aan wordt gezet

automationManager.addRule(rule_motion_wasmachine_light())