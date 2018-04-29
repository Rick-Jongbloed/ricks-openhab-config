scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
from openhab.triggers import ItemStateUpdateTrigger, ItemCommandTrigger, ItemStateChangeTrigger, StartupTrigger
from openhab.actions import Mqtt, Pushover

class rule_kantoor_motion (SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            StartupTrigger(),
                            ItemCommandTrigger("timer_rule_kantoor_motion_init_hardware", command="OFF"),
                            ItemStateUpdateTrigger("sensor_motion_office_motion_status", state="ON"),
                            ItemCommandTrigger("timer_rule_kantoor_motion_detected_motion", command="OFF")
                        ]

    def execute(self, module, input):
        logging.info(input)

        # initialize programmable items
        if str(items.timer_rule_kantoor_motion_detected_motion) == "NULL":
            events.postUpdate("timer_rule_kantoor_motion_detected_motion","OFF")

#       #initialize non-pollable items
        if str(items.sensor_motion_office_motion_status) == "NULL":
            events.postUpdate("sensor_motion_office_motion_status","OFF")
        
        # no hardware initialize timer needed yet

        # if motion trigger is started.... 
        if "event" in input:
            trigger = str(input['event'])        
        else:
            trigger = "startup"
        logging.info(trigger)

        if "sensor_motion_office_motion_status" in trigger:
            logging.info("Kantoor: Motion detected. (Re)setting timer and keeping light on for 5 minutes")
            events.sendCommand("timer_rule_kantoor_motion_detected_motion", "ON")
        elif "timer_rule_kantoor_motion_detected_motion" in trigger:
            logging.info("Motion niet meer detected")

automationManager.addRule(rule_kantoor_motion())

class rule_kantoor_pc_monitors (SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            StartupTrigger(),
                            ItemCommandTrigger("timer_rule_automate_ventilation_new_init_hardware", command="OFF"),
                            ItemStateChangeTrigger("kantoor_pc_net_online"),
                            ItemCommandTrigger("timer_rule_kantoor_motion_detected_motion")
                        ]

    def execute(self, module, input):
        #logging.info(input)
        
        # init
        if str(items.switch_kantoor_pc_monitors_toggle) == "NULL" or str(items.kantoor_pc_net_online) == "NULL":
            
            if str(items.switch_kantoor_pc_monitors_toggle) == "NULL":
                logging.info("Switch monitors kantoor pc is in an unknown state, pending refresh")
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_monitors_beast" + "/status", "0")

            if str(items.kantoor_pc_net_online) == "NULL":
                logging.info("Kantoor PC network status is in an unknown state, pending refresh")
            events.sendCommand("timer_rule_kantoor_monitors_init_hardware","ON")

    	else:
            # start of procedure
            logging.info("**** kantoor_pc_net_online rule running due to state change in pc or motion (or startup)")

            if items.timer_rule_kantoor_motion_detected_motion == OFF and items.switch_kantoor_pc_monitors_toggle == ON:
                logging.info("**** timer_rule_kantoor_motion_detected_motion turned to OFF, switch_kantoor_pc_monitors_toggle is ON, TURNING switch_kantoor_pc_monitors_toggle OFF ****")
                events.sendCommand("switch_kantoor_pc_monitors_toggle", "OFF")
            
            elif items.kantoor_pc_net_online == ON and items.switch_kantoor_pc_monitors_toggle == OFF and items.timer_rule_kantoor_motion_detected_motion != OFF:
                logging.info("**** kantoor_pc_net_online is ON, switch_kantoor_pc_monitors_toggle is OFF, TURNING switch_kantoor_pc_monitors_toggle ON ****")
                events.sendCommand("switch_kantoor_pc_monitors_toggle", "ON")
                
            elif items.kantoor_pc_net_online == OFF and items.switch_kantoor_pc_monitors_toggle == ON:
                logging.info("**** kantoor_pc_net_online is OFF, switch_kantoor_pc_monitors_toggle is ON, TURNING switch_kantoor_pc_monitors_toggle OFF ****")
                events.sendCommand("switch_kantoor_pc_monitors_toggle", "OFF")
            else:
                logging.info("Rule kantoor PC monitors evaluated, but no change needed")
                pass

automationManager.addRule(rule_kantoor_pc_monitors())