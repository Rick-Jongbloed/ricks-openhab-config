from core.log import logging, LOG_PREFIX
from core.rules import rule
from core.triggers import when
from core.actions import Pushover
from time import sleep

# STARTUP RULE SHOULD BE ADDED...
@rule("Ventilation automation")
@when("Item number_ventilator_level_set_manual received command")
@when("Item switch_ventilator_level_toggle_auto changed from OFF to ON")
@when("Item humid_status_badkamer_sensor changed")
@when("Item timer_rule_automate_ventilation_new_init_hardware received command OFF")
def rule_automate_ventilation_new(event):
    log = logging.getLogger(LOG_PREFIX + ".ventilation_automation")
    log.debug("TRIGGER: " + str(event))  
    log.debug("@@@@ switch_ventilator_level_toggle_auto: " + str(items.switch_ventilator_level_toggle_auto))
    # special logic to define automatic/manual
    if "number_ventilator_level_set_manual" in str(event):
        level_gui_manual = str(event).split()[-1]
        if level_gui_manual == "4":

            #if str(items.switch_ventilator_level_toggle_auto) == "OFF":
            log.info("POSTUPDATING AUTO TO ON")
            events.postUpdate("switch_ventilator_level_toggle_auto", "ON")
            #Pushover.pushover("Ventilatie status: autosensing", "Telefoon_prive_rick01")  
            sleep(0.5)
            log.info("MANUAL = 4, switch_ventilator_level_toggle_auto: " + str(level_gui_manual))
        else:
            #if str(items.switch_ventilator_level_toggle_auto) == "ON":
            events.sendCommand("switch_ventilator_level_toggle_auto", "OFF")  
            Pushover.pushover("Ventilatie status: override (20m) gestart", "Telefoon_prive_rick01")  
            sleep(0.5)
#                   logging.info("MANUAL IS NOT 4, switch_ventilator_level_toggle_auto: " + str(level_gui_manual))
    elif "switch_ventilator_level_toggle_auto" in str(event):
        #logging.debug("CATHCA")
        Pushover.pushover("Ventilatie status: override (20m) verlopen", "Telefoon_prive_rick01")  
    # reporting logic stuff
    log.debug("@@@@ number_ventilator_level_set_manual: " + str(items.number_ventilator_level_set_manual))
    log.debug("@@@@ humid_status_badkamer_sensor: " + str(items.humid_status_badkamer_sensor))

    # # reporting hardware stuff
    log.debug("@@@@ switch_ventilator_toggle_1_startup_state: " + str(items.switch_ventilator_toggle_1_startup_state))
    log.debug("@@@@ switch_ventilator_toggle_1: " + str(items.switch_ventilator_toggle_1_startup_state))
    log.debug("@@@@ switch_ventilator_toggle_2_startup_state: " + str(items.switch_ventilator_toggle_2_startup_state))
    log.debug("@@@@ switch_ventilator_toggle_1: " + str(items.switch_ventilator_toggle_1_startup_state))
    

    # initializing hardware stuff
    if str(items.switch_ventilator_toggle_1_startup_state) == "NULL" or str(items.switch_ventilator_toggle_2_startup_state) == "NULL":
        
        # extra switch (status_rule_automate_ventilation_init) voor status
        #if (items.status_rule_automate_ventilation_init_counter == "NULL" or items.status_rule_automate_ventilation_init_counter == "Initialized"):
        #    logging.debug("@@@@ status_rule_automate_ventilation_init_counter: " + str(items.status_rule_automate_ventilation_init_counter))
        #    counter = 0
        #    logging.debug("@@@@ counter variable: " + str(counter))
        #    #events.postUpdate("status_rule_automate_ventilation_init_counter",counter)
        #else:
        #    logging.debug("@@@@ status_rule_automate_ventilation_init_counter: " + str(items.status_rule_automate_ventilation_init_counter))
        #    counter = items.status_rule_automate_ventilation_init_counter + 1
        #    logging.debug("@@@@ counter variable: " + str(counter))
        #
        #events.postUpdate("status_rule_automate_ventilation_init_counter",items.status_rule_automate_ventilation_init_counter + 1)

        # poll mqtt device
        log.debug("@@@@ Devices are in unknown state, polling MQTT")
        actions.get("mqtt", "mqtt:broker:local").publishMQTT("cmnd/" + "sonoff_switch_ventilatie" + "/status", "0")
        # Reschedule in 30 seconds until the items are in a proper state
        events.sendCommand("timer_rule_automate_ventilation_new_init_hardware","ON")
    else:
        if str(items.humid_status_badkamer_sensor) == "NULL":
            log.debug("@@@@ Humidity sensor is in unknown state, waiting for update (30s)")
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
                        log.debug("POSTUPDATING AUTO TO ON")
                        events.postUpdate("switch_ventilator_level_toggle_auto","ON")
                        #Pushover.pushover("Ventilatie status: autosensing", "Telefoon_prive_rick01")  
                    # assume automatic mode = on
                    log.info("@@@@ Automatic mode: ON")
                    
                    # calculate setting 
                    if str(items.humid_status_badkamer_sensor) == "WET":
                        log.debug("@@@@ rule_automate_ventilation_new setting level to 3....")
                        # must use class to calculate this, with a return value (in -> WET, OUT 3)
                        # then: in another class: in 3 -> set switches -> out OK, for now, hardcode
                        events.sendCommand("number_ventilator_level_set", "3")
                        events.postUpdate("number_ventilator_level_set_manual", "3")
                    else: 
                        
                        # state is COMFORT or DRY
                        log.debug("@@@@ rule_automate_ventilation_new setting level to 1....")
                        events.sendCommand("number_ventilator_level_set", "1")
                        events.postUpdate("number_ventilator_level_set_manual", "1")
                else:
                    # Manual mode
                    log.debug("Automatic mode: OFF | Setting: " + str(items.number_ventilator_level_set_manual))
                    events.sendCommand("number_ventilator_level_set", str(items.number_ventilator_level_set_manual))   

@rule("Ventilation set level")
@when("Item number_ventilator_level_set received command")
def number_ventilator_level_set(event):
        # ventilatiefunctie zou alleen de switches mogen zetten als deze nog niet zijn ingesteld
        log = logging.getLogger(LOG_PREFIX + ".number_ventilator_level_set")
        log.debug(event)
        level_ventilation = str(event).split()[-1]
        log.debug(str(level_ventilation))
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
            log.info("!!!! number_ventilator_level_set is changed, but couldn't be matched to a correct state: '" + str(level_ventilation) + "'")



# class rule_switch_ventilator_level_set_manual_alexa(SimpleRule):
#     def __init__(self):
#         self.triggers = [ 
#                             ItemCommandTrigger("switch_ventilator_level_set_manual_alexa", command="ON").trigger,
#                             ItemCommandTrigger("switch_ventilator_level_set_manual_alexa", command="OFF").trigger 
#                         ]
#     def execute(self, module, inputs):
        
#         # ventilatiefunctie zou alleen de switches mogen zetten als deze nog niet zijn ingesteld
# #        logging.info(input)
#         command = inputs['command']
# #        logging.info(str(level_ventilation))
#         if command == "ON":
#             events.sendCommand("number_ventilator_level_set_manual", "3")
#         else:
#             events.sendCommand("number_ventilator_level_set_manual", "4")
# automationManager.addRule(rule_switch_ventilator_level_set_manual_alexa())