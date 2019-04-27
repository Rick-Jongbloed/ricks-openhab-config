scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")
from core.log import logging, LOG_PREFIX
from core.triggers import StartupTrigger, ItemStateChangeTrigger, ItemCommandTrigger
from time import sleep
from core.actions import Pushover

class rule_automate_ventilation_new(SimpleRule):
    def __init__(self):
        self.triggers = [                                                     
                            ItemCommandTrigger("timer_rule_automate_ventilation_new_init_hardware", command="OFF").trigger,                       # GUI instellingen      
                            ItemCommandTrigger("number_ventilator_level_set_manual").trigger,                       # GUI instellingen      
                            ItemStateChangeTrigger("switch_ventilator_level_toggle_auto", state="ON", previousState="OFF").trigger,      # Manual mode gaat uit na 20 minuten
                            ItemStateChangeTrigger("humid_status_badkamer_sensor").trigger,   # luchtvochtigheid verandert in badkamer
                            StartupTrigger().trigger                             # Run on startup to initialize, will reset the timer(!)
                        ]
    def execute(self, module, inputs):
        log = logging.getLogger(LOG_PREFIX + ".test_logging_script")
        
        # reporting and logic on trigger
        self.log.info("TRIGGER: " + str(inputs))  
        log.info("TRIGGER: " + str(inputs))  
        logging.info("@@@@ switch_ventilator_level_toggle_auto: " + str(items.switch_ventilator_level_toggle_auto))
        # special logic to define automatic/manual
        if "event" in inputs:
            if "number_ventilator_level_set_manual" in str(inputs['event']):
                level_gui_manual = str(inputs['command'])
                logging.info(level_gui_manual)
                if level_gui_manual == "4":

                    #if str(items.switch_ventilator_level_toggle_auto) == "OFF":
                    logging.info("POSTUPDATING AUTO TO ON")
                    events.postUpdate("switch_ventilator_level_toggle_auto", "ON")
                    #Pushover.pushover("Ventilatie status: autosensing", "Telefoon_prive_rick01")  
                    sleep(0.5)
                    logging.info("MANUAL = 4, switch_ventilator_level_toggle_auto: " + str(level_gui_manual))
                else:
                    #if str(items.switch_ventilator_level_toggle_auto) == "ON":
                    events.sendCommand("switch_ventilator_level_toggle_auto", "OFF")  
                    Pushover.pushover("Ventilatie status: override (20m) gestart", "Telefoon_prive_rick01")  
                    sleep(0.5)
 #                   logging.info("MANUAL IS NOT 4, switch_ventilator_level_toggle_auto: " + str(level_gui_manual))
            elif "switch_ventilator_level_toggle_auto" in str(inputs['event']):
                #logging.info("CATHCA")
                Pushover.pushover("Ventilatie status: override (20m) verlopen", "Telefoon_prive_rick01")  
        # reporting logic stuff
        # logging.info("@@@@ number_ventilator_level_set_manual: " + str(items.number_ventilator_level_set_manual))
        

        # logging.info("@@@@ humid_status_badkamer_sensor: " + str(items.humid_status_badkamer_sensor))

        # # reporting hardware stuff
        logging.info("@@@@ switch_ventilator_toggle_1_startup_state: " + str(items.switch_ventilator_toggle_1_startup_state))
        logging.info("@@@@ switch_ventilator_toggle_1: " + str(items.switch_ventilator_toggle_1_startup_state))
        logging.info("@@@@ switch_ventilator_toggle_2_startup_state: " + str(items.switch_ventilator_toggle_2_startup_state))
        logging.info("@@@@ switch_ventilator_toggle_1: " + str(items.switch_ventilator_toggle_1_startup_state))
        

        # initializing hardware stuff
        if str(items.switch_ventilator_toggle_1_startup_state) == "NULL" or str(items.switch_ventilator_toggle_1_startup_state) == "NULL":
            
            # extra switch (status_rule_automate_ventilation_init) voor status
            #if (items.status_rule_automate_ventilation_init_counter == "NULL" or items.status_rule_automate_ventilation_init_counter == "Initialized"):
            #    logging.info("@@@@ status_rule_automate_ventilation_init_counter: " + str(items.status_rule_automate_ventilation_init_counter))
            #    counter = 0
            #    logging.info("@@@@ counter variable: " + str(counter))
            #    #events.postUpdate("status_rule_automate_ventilation_init_counter",counter)
            #else:
            #    logging.info("@@@@ status_rule_automate_ventilation_init_counter: " + str(items.status_rule_automate_ventilation_init_counter))
            #    counter = items.status_rule_automate_ventilation_init_counter + 1
            #    logging.info("@@@@ counter variable: " + str(counter))
            #
            #events.postUpdate("status_rule_automate_ventilation_init_counter",items.status_rule_automate_ventilation_init_counter + 1)

            # poll mqtt device
            logging.info("@@@@ Devices are in unknown state, polling MQTT")
            Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_ventilatie" + "/status", "0")
            
            # Reschedule in 30 seconds until the items are in a proper state
            events.sendCommand("timer_rule_automate_ventilation_new_init_hardware","ON")
        else:
            if str(items.humid_status_badkamer_sensor) == "NULL":
                logging.info("@@@@ Humidity sensor is in unknown state, waiting for update (30s)")
                events.sendCommand("timer_rule_automate_ventilation_new_init_hardware","ON")

            else:
                # only continue if all the hardware switches are initialized
                if str(items.switch_ventilator_toggle_2) != "NULL" and str(items.switch_ventilator_toggle_2) != "NULL" and str(items.humid_status_badkamer_sensor) != "NULL":
                    
                    # Turn off timer if it's still running
                    if str(items.timer_rule_automate_ventilation_new_init_hardware) != "OFF":
                        events.postUpdate("timer_rule_automate_ventilation_new_init_hardware","OFF")
                         
                    #   Setup automatic mode
                    if items.switch_ventilator_level_toggle_auto != OFF:
                    
                        # initialize automatic mode if needed
                        if str(items.switch_ventilator_level_toggle_auto) == "NULL":
                            logging.info("POSTUPDATING AUTO TO ON")
                            events.postUpdate("switch_ventilator_level_toggle_auto","ON")
                            #Pushover.pushover("Ventilatie status: autosensing", "Telefoon_prive_rick01")  
                        # assume automatic mode = on
    #                    logging.info("@@@@ Automatic mode: ON")
                        
                        # calculate setting 
                        if str(items.humid_status_badkamer_sensor) == "WET":
   #                         logging.info("@@@@ rule_automate_ventilation_new setting level to 3....")
                            # must use class to calculate this, with a return value (in -> WET, OUT 3)
                            # then: in another class: in 3 -> set switches -> out OK, for now, hardcode
                            events.sendCommand("number_ventilator_level_set", "3")
                            events.postUpdate("number_ventilator_level_set_manual", "3")
                        else: 
                            
                            # state is COMFORT or DRY
  #                          logging.info("@@@@ rule_automate_ventilation_new setting level to 1....")
                            events.sendCommand("number_ventilator_level_set", "1")
                            events.postUpdate("number_ventilator_level_set_manual", "1")
                    else:
                        # Manual mode
 #                       logging.info("Automatic mode: OFF | Setting: " + str(items.number_ventilator_level_set_manual))
                        events.sendCommand("number_ventilator_level_set", str(items.number_ventilator_level_set_manual))   
#                else:
                    # can't really happen
#                    pass
automationManager.addRule(rule_automate_ventilation_new())



class number_ventilator_level_set(SimpleRule):
    def __init__(self):
        self.triggers = [ ItemCommandTrigger("number_ventilator_level_set").trigger ]
    def execute(self, module, inputs):
    
        # ventilatiefunctie zou alleen de switches mogen zetten als deze nog niet zijn ingesteld
#        logging.info(input)
        level_ventilation = inputs['command']
#        logging.info(str(level_ventilation))
        if str(level_ventilation) == "1":
            events.sendCommand("switch_ventilator_toggle_1", "OFF")
            events.sendCommand("switch_ventilator_toggle_2", "OFF")
        elif str(level_ventilation) == "2":
            events.sendCommand("switch_ventilator_toggle_2", "OFF")
            sleep(0.5)
            events.sendCommand("switch_ventilator_toggle_1", "ON")
        elif str(level_ventilation) == "3":
            events.sendCommand("switch_ventilator_toggle_1", "OFF")
            sleep(0.5)
            events.sendCommand("switch_ventilator_toggle_2", "ON")
        else:
            logging.info("!!!! number_ventilator_level_set is changed, but couldn't be matched to a correct state: '" + str(level_ventilation) + "'")
automationManager.addRule(number_ventilator_level_set())


class rule_switch_ventilator_level_set_manual_alexa(SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            ItemCommandTrigger("switch_ventilator_level_set_manual_alexa", command="ON").trigger,
                            ItemCommandTrigger("switch_ventilator_level_set_manual_alexa", command="OFF").trigger 
                        ]
    def execute(self, module, inputs):
        
        # ventilatiefunctie zou alleen de switches mogen zetten als deze nog niet zijn ingesteld
#        logging.info(input)
        command = inputs['command']
#        logging.info(str(level_ventilation))
        if command == "ON":
            events.sendCommand("number_ventilator_level_set_manual", "3")
        else:
            events.sendCommand("number_ventilator_level_set_manual", "4")
automationManager.addRule(rule_switch_ventilator_level_set_manual_alexa())