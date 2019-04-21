
scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
#from openhab.triggers import StartupTrigger, ItemStateChangeTrigger, ItemCommandTrigger, item_triggered, ITEM_COMMAND, ItemStateUpdateTrigger
from openhab.triggers import ItemStateChangeTrigger, ItemCommandTrigger, item_triggered, ITEM_COMMAND, ItemStateUpdateTrigger
from lucid.triggers import StartupTrigger

from openhab.actions import Mqtt, Pushover
from time import sleep
     
class rule_automate_keuken_licht(SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            StartupTrigger(),                                                                                           # Run on startup to initialize, will reset the timer(!)
                            ItemCommandTrigger("timer_rule_automate_keuken_licht_init_hardware", command="OFF"),                          # init hardware, only run rule when zwave is initialized     
                            ItemStateChangeTrigger("light_keuken_dimmer_plafond_toggle"),                                                        # monitor changes in het licht    
                            ItemStateUpdateTrigger("sensor_motion_keuken_motion_status")#,                                        # motion
                         #   ItemStateUpdateTrigger("sensor_motion_keuken_woonkamer_motion_status")                                        # motion
                        ]
    def execute(self, module, input):        
        logging.info("rule_automate_keuken_licht started")
        if str(items.timer_rule_automate_keuken_licht_off) == "NULL":                                                                     # initialize timer (set to off, so it's initialized)
            events.sendCommand("timer_rule_automate_keuken_licht_off","OFF")                
        if str(items.sensor_motion_keuken_motion_status) == "NULL":                                                              # initializing hardware stuff
            events.sendCommand("sensor_motion_keuken_motion_status","OFF")   
        # if str(items.sensor_motion_keuken_woonkamer_motion_status) == "NULL":
        #     events.sendCommand("sensor_motion_keuken_woonkamer_motion_status","OFF")  
        if str(items.light_keuken_dimmer_plafond_toggle) == "NULL":                                                                              
            logging.info("@@@@ rule_automate_keuken_licht: Light device is in unknown state, rescheduling rule")
            events.sendCommand("timer_rule_automate_keuken_licht_init_hardware","ON")                                                     # Reschedule in 30 seconds until the items are in a proper state
        else:
            if str(items.timer_rule_automate_keuken_licht_init_hardware) != "OFF":                                                        # Turn off timer if it's still running
                events.postUpdate("timer_rule_automate_keuken_licht_init_hardware","OFF")
            if str(items.light_keuken_dimmer_plafond_toggle) == "ON":                                                                            # if light is on, but timer is off, set timer
                if str(items.timer_rule_automate_keuken_licht_off) == "OFF":
                    logging.info("@@@@ rule_automate_keuken_licht: Light is on but timer is off, setting timer to 2 minutes...")
                    events.sendCommand("timer_rule_automate_keuken_licht_off","ON")
                else:
                    if "event" in input and "motion" in str(input['event']):                                                           # timer is on. check if event is triggered by motion, if so, enable timer                         
                        logging.info("@@@@ rule_automate_keuken_licht: Motion sensors triggered, extending timer with 5 minutes...")
                        events.sendCommand("timer_rule_automate_keuken_licht_off","ON")               
automationManager.addRule(rule_automate_keuken_licht())
 
class rule_automate_keuken_licht_timer_expired(SimpleRule):
    def __init__(self):
        self.triggers = [ ItemStateChangeTrigger("timer_rule_automate_keuken_licht_off",state="OFF", previousState="ON") ]           # Licht moet uit na 5 minuten, de uitvoer in het script is het meest compleet.
    def execute(self, module, input):
        logging.info("@@@@ Timer has expired: timer_rule_automate_keuken_licht_off")
        events.sendCommand("light_keuken_dimmer_plafond_toggle", "OFF")
automationManager.addRule(rule_automate_keuken_licht_timer_expired())