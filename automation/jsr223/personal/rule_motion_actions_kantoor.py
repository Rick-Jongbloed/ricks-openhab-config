scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
#from openhab.triggers import ItemStateUpdateTrigger, ItemCommandTrigger, ItemStateChangeTrigger, StartupTrigger
from openhab.triggers import ItemStateUpdateTrigger, ItemCommandTrigger, ItemStateChangeTrigger
from lucid.triggers import StartupTrigger
from openhab.actions import Mqtt, Pushover

class rule_kantoor_motion (SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            StartupTrigger(),
                            ItemCommandTrigger("timer_rule_kantoor_motion_init_hardware", command="OFF"),
                            ItemStateUpdateTrigger("sensor_motion_office_motion_status", state="ON"),
                            ItemStateUpdateTrigger("sensor_motion_office_plafond_motion_status", state="ON"),   #new
                        #    ItemCommandTrigger("timer_rule_kantoor_motion_detected_motion", command="OFF")         # niet nodig?
                        ]

    def execute(self, module, input):
        #logging.info(input)

        # initialize programmable items
        if str(items.timer_rule_kantoor_motion_detected_motion) == "NULL":
            events.postUpdate("timer_rule_kantoor_motion_detected_motion","OFF")

#       #initialize non-pollable items
        if str(items.sensor_motion_office_motion_status) == "NULL":
            events.postUpdate("sensor_motion_office_motion_status","OFF")
        if str(items.sensor_motion_office_plafond_motion_status) == "NULL":
            events.postUpdate("sensor_motion_office_plafond_motion_status","OFF")
        # no hardware initialize timer needed yet

        # if motion trigger is started.... 
        if "event" in input:
            trigger = str(input['event'])        
        else:
            trigger = "startup"
        #logging.info(trigger)

        if "sensor_motion_office_motion_status" in trigger or "sensor_motion_office_plafond_motion_status" in trigger:
            logging.info("Kantoor: Motion detected. (Re)setting timer and keeping light on for 5 minutes")
            events.sendCommand("timer_rule_kantoor_motion_detected_motion", "ON")
        #elif "timer_rule_kantoor_motion_detected_motion" in trigger:
        #    logging.info("Motion niet meer detected")

automationManager.addRule(rule_kantoor_motion())

class rule_kantoor_pc_monitors (SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            StartupTrigger(),
                            ItemCommandTrigger("timer_rule_kantoor_monitors_init_hardware", command="OFF"),
                            ItemStateChangeTrigger("kantoor_pc_net_online"),
                            ItemStateChangeTrigger("light_plafond_kantoor_rechts_toggle"),
                            ItemStateChangeTrigger("light_plafond_kantoor_midden_toggle"),
                            ItemStateChangeTrigger("light_plafond_kantoor_links_toggle"),
                            ItemStateChangeTrigger("kantoor_pc_net_online"),
                            ItemCommandTrigger("timer_rule_kantoor_motion_detected_motion", commsnd="ON")
                            # timer_rule_kantoor_motion_override_cooldowm 
                        ]

    def execute(self, module, input):
        #logging.info(input)
        
        # init
        if str(items.switch_kantoor_pc_monitors_toggle) == "NULL" or str(items.kantoor_pc_net_online) == "NULL" or str(items.light_plafond_kantoor_links_toggle) == "NULL" or str(items.light_plafond_kantoor_midden_toggle) == "NULL" or str(items.light_plafond_kantoor_links_toggle) == "NULL":
            
            if str(items.switch_kantoor_pc_monitors_toggle) == "NULL":
                logging.info("Switch monitors kantoor pc is in an unknown state, pending refresh")
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_monitors_beast" + "/status", "0")

            if str(items.kantoor_pc_net_online) == "NULL":
                logging.info("Kantoor PC network status is in an unknown state, pending refresh")
            events.sendCommand("timer_rule_kantoor_monitors_init_hardware","ON")

            if str(items.light_plafond_kantoor_links_toggle) == "NULL":
                logging.info("Kantoor lamp links is in an unknown state, pending refresh")
            events.sendCommand("timer_rule_kantoor_monitors_init_hardware","ON")

            if str(items.light_plafond_kantoor_midden_toggle) == "NULL":
                logging.info("Kantoor lamp midden is in an unknown state, pending refresh")
            events.sendCommand("timer_rule_kantoor_monitors_init_hardware","ON")

            if str(items.light_plafond_kantoor_links_toggle) == "NULL":
                logging.info("Kantoor lamp rechts is in an unknown state, pending refresh")
            events.sendCommand("timer_rule_kantoor_monitors_init_hardware","ON")

    	else:
            # start of procedure
            logging.info("**** kantoor_pc_net_online rule running due to state change in pc,lights or motion (or startup)")

            if items.timer_rule_kantoor_motion_detected_motion == OFF:
                if items.switch_kantoor_pc_monitors_toggle == ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned to OFF, switch_kantoor_pc_monitors_toggle is ON, TURNING switch_kantoor_pc_monitors_toggle OFF ****")
                    events.sendCommand("switch_kantoor_pc_monitors_toggle", "OFF")
                if items.light_plafond_kantoor_links_toggle == ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned to OFF, light_plafond_kantoor_links_toggle is ON, TURNING light_plafond_kantoor_links_toggle OFF ****")
                    events.sendCommand("light_plafond_kantoor_links_toggle", "OFF")
                if items.light_plafond_kantoor_midden_toggle == ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned to OFF, light_plafond_kantoor_midden_toggle is ON, TURNING light_plafond_kantoor_midden_toggle OFF ****")
                    events.sendCommand("light_plafond_kantoor_midden_toggle", "OFF")
                if items.light_plafond_kantoor_rechts_toggle == ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned to OFF, light_plafond_kantoor_rechts_toggle is ON, TURNING light_plafond_kantoor_rechts_toggle OFF ****")
                    events.sendCommand("light_plafond_kantoor_rechts_toggle", "OFF")
            
            elif items.timer_rule_kantoor_motion_detected_motion != OFF:
                if items.kantoor_pc_net_online == ON and items.switch_kantoor_pc_monitors_toggle == OFF:
                    logging.info(items.switch_kantoor_pc_monitors_toggle)
                    logging.info("**** kantoor_pc_net_online is ON, switch_kantoor_pc_monitors_toggle is OFF, TURNING switch_kantoor_pc_monitors_toggle ON ****")
                    events.sendCommand("switch_kantoor_pc_monitors_toggle", "ON")
                if items.light_plafond_kantoor_links_toggle != ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned ON, light_plafond_kantoor_links_toggle is OFF, TURNING light_plafond_kantoor_links_toggle ON ****")
                    events.sendCommand("light_plafond_kantoor_links_toggle", "ON")
                if items.light_plafond_kantoor_midden_toggle != ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned ON, light_plafond_kantoor_midden_toggle is OFF, TURNING light_plafond_kantoor_midden_toggle ON ****")
                    events.sendCommand("light_plafond_kantoor_midden_toggle", "ON")
                if items.light_plafond_kantoor_rechts_toggle != ON:
                    logging.info("**** timer_rule_kantoor_motion_detected_motion turned ON, light_plafond_kantoor_rechts_toggle is OFF, TURNING light_plafond_kantoor_rechts_toggle ON ****")
                    events.sendCommand("light_plafond_kantoor_rechts_toggle", "ON")

            elif items.kantoor_pc_net_online == OFF and items.switch_kantoor_pc_monitors_toggle == ON:
                logging.info("**** kantoor_pc_net_online is OFF, switch_kantoor_pc_monitors_toggle is ON, TURNING switch_kantoor_pc_monitors_toggle OFF ****")
                events.sendCommand("switch_kantoor_pc_monitors_toggle", "OFF")
            else:
                #logging.info("Rule kantoor PC monitors evaluated, but no change needed")
                pass

automationManager.addRule(rule_kantoor_pc_monitors())