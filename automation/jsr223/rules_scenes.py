scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
from openhab.triggers import ItemStateChangeTrigger, ItemCommandTrigger, StartupTrigger
from openhab.actions import Mqtt, Pushover

class rule_scene_lights_living (SimpleRule):
    def __init__(self):
        self.triggers = [ 
                            StartupTrigger(), 
                            
                            ItemCommandTrigger("timer_rule_scene_woonkamer_new_init_hardware", command="OFF"),

                            ItemStateChangeTrigger("light_woonkamer_dimmer_boekenkast"),
                            ItemStateChangeTrigger("light_woonkamer_dimmer_vitrinekast"),
                            ItemStateChangeTrigger("switch_led_strip_tv_toggle", state="ON",previousState="OFF"),
                            ItemStateChangeTrigger("switch_groene_tl_toggle", state="ON",previousState="OFF"),
                            ItemStateChangeTrigger("switch_led_strip_tv_toggle", state="OFF",previousState="ON"),
                            ItemStateChangeTrigger("switch_groene_tl_toggle", state="OFF",previousState="ON"),

                            ItemCommandTrigger("number_scene_lights_living"),
                            ItemCommandTrigger("switch_scene_living_chill"),
                            ItemCommandTrigger("switch_scene_living_full")
                        ]

    def execute(self, module, input):
        logging.info("STARTED")
        
        ######################################################################################
        # initialize programmable items
        if str(items.timer_rule_scene_woonkamer_new_init_hardware) == "NULL":
            events.postUpdate("timer_rule_scene_woonkamer_new_init_hardware","OFF")    
        #if str(items.timer_rule_scene_woonkamer_disable_detection) == "NULL":
            #events.postUpdate("timer_rule_scene_woonkamer_disable_detection","OFF")  

        # check if devices are null...
        if str(items.light_woonkamer_dimmer_boekenkast) == "NULL" or str(items.light_woonkamer_dimmer_vitrinekast) == "NULL" or str(items.switch_led_strip_tv_toggle) == "NULL" or str(items.switch_groene_tl_toggle) == "NULL":
            if str(items.light_woonkamer_dimmer_boekenkast) == "NULL":
                logging.info("Dimmer boekenkast is in unknown state, pending refresh")
            if str(items.light_woonkamer_dimmer_vitrinekast) == "NULL":
                logging.info("Dimmer vitrinekast is in unknown state, pending refresh")
            if str(items.switch_led_strip_tv_toggle) == "NULL":
                logging.info("Led strip TV is in unknown state, polling MQTT")
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_ledstrip_tv" + "/status", "0")
            if str(items.switch_groene_tl_toggle) == "NULL":
                logging.info("Groene TL is in unknown state, polling MQTT")
                Mqtt.publish("mosquitto", "cmnd/" + "sonoff_green_tl" + "/status", "0")
                        
            # Reschedule in 30 seconds until the items are in a proper state, if timer is somehow not yet running
            if items.timer_rule_scene_woonkamer_new_init_hardware != ON:
                events.sendCommand("timer_rule_scene_woonkamer_new_init_hardware","ON")
        #######################################################################################
        else:           
            # set scene number to scene and execute commands
            logging.info(input)
            scene_number = ""
            command = ""
            if "event" in input:
                trigger = str(input['event'])
                if "number_scene_lights_living" in trigger:
                    scene_number = str(input['command'])
                    #logging.info("Recieved command from GUI(" + str(scene_number) + ")") 
                    #logging.info("1 timer_rule_scene_woonkamer_new_gui_set_new_scene: " + str(items.timer_rule_scene_woonkamer_new_gui_set_new_scene))
                    #events.sendCommand("timer_rule_scene_woonkamer_disable_detection", "ON")
                elif "switch_scene_living_chill" in trigger or "switch_scene_living_full" in trigger:
                    if input['command'] == OFF:
                        scene_number = "1"
                    
                    #logging.info("2 timer_rule_scene_woonkamer_new_gui_set_new_scene: " + str(items.timer_rule_scene_woonkamer_new_gui_set_new_scene))
                    #if items.timer_rule_scene_woonkamer_new_gui_set_new_scene == ON:
                        #logging.info("timer is running, quitting script")
            else:
                trigger = "startup"
            
            #######################################################################################
            #logging.info(trigger)
            # # device states
            # logging.info("**** input Device states:")
            # logging.info("input light_woonkamer_dimmer_boekenkast: " + str(items.light_woonkamer_dimmer_boekenkast))
            # logging.info("input light_woonkamer_dimmer_vitrinekast: " + str(items.light_woonkamer_dimmer_vitrinekast))
            # logging.info("input switch_led_strip_tv_toggle: " + str(items.switch_led_strip_tv_toggle))
            # logging.info("input switch_groene_tl_toggle: " + str(items.switch_groene_tl_toggle))

            # # input variables
            # logging.info("**** input scene states:")
            # logging.info("input number_scene_lights_living: " + str(items.number_scene_lights_living))
            # logging.info("input switch_scene_living_chill: " + str(items.switch_scene_living_chill))
            # logging.info("input switch_scene_living_full: " + str(items.switch_scene_living_full))

            
            # skip processing if number_scene_lights_living received command
            #if items.timer_rule_scene_woonkamer_disable_detection == OFF:
            if trigger == "startup":
                if str(items.light_woonkamer_dimmer_boekenkast) == "0" and str(items.light_woonkamer_dimmer_vitrinekast) == "0" and items.switch_led_strip_tv_toggle == OFF and items.switch_groene_tl_toggle == OFF:
                    scene_number = "1"
                elif str(items.light_woonkamer_dimmer_boekenkast) == "30" and str(items.light_woonkamer_dimmer_vitrinekast) == "30" and items.switch_led_strip_tv_toggle == ON and items.switch_groene_tl_toggle == ON:
                    scene_number = "2"
                elif str(items.light_woonkamer_dimmer_boekenkast) == "100" and str(items.light_woonkamer_dimmer_vitrinekast) == "100" and items.switch_led_strip_tv_toggle == OFF and items.switch_groene_tl_toggle == OFF:
                    scene_number = "3"
                else:
                    scene_number = "4"
            #######################################################################################

           #logging.info(scene_number)
            #detect which event has triggered the rule)
            if scene_number == "1":
                if items.number_scene_lights_living != 1:
                    events.postUpdate("number_scene_lights_living", "1")
                
                # uitvoeren switch acties
                if items.switch_scene_living_chill != OFF:
                    events.postUpdate("switch_scene_living_chill",  "OFF")
                if items.switch_scene_living_full != OFF:    
                    events.postUpdate("switch_scene_living_full",   "OFF")

                # uitvoeren device acties # status is net gedetecteerd, dus worden hier niet ingesteld, hoef niks te doen
                if (str(items.light_woonkamer_dimmer_boekenkast) != "0"):
                    events.sendCommand("light_woonkamer_dimmer_boekenkast", "OFF")
                if (str(items.light_woonkamer_dimmer_vitrinekast) != "0"):
                    events.sendCommand("light_woonkamer_dimmer_vitrinekast", "OFF")
                if items.switch_led_strip_tv_toggle != OFF:
                    events.sendCommand("switch_led_strip_tv_toggle", "OFF")
                if items.switch_groene_tl_toggle != OFF:
                    events.sendCommand("switch_groene_tl_toggle", "OFF")

            elif "switch_scene_living_chill" in trigger or scene_number == "2":
                if items.number_scene_lights_living != 2:
                    events.postUpdate("number_scene_lights_living", "2")
                
                # uitvoeren switch acties
                if items.switch_scene_living_chill != ON:
                    events.postUpdate("switch_scene_living_chill",  "ON")
                if items.switch_scene_living_full != OFF:
                    events.postUpdate("switch_scene_living_full",   "OFF")
                
                # uitvoeren device acties
                if (str(items.light_woonkamer_dimmer_boekenkast) != "30"):
                    #events.sendCommand("light_woonkamer_dimmer_boekenkast", "30")
                    events.sendCommand("light_woonkamer_dimmer_boekenkast", "30")
                if (str(items.light_woonkamer_dimmer_vitrinekast) != "30"):
                    events.sendCommand("light_woonkamer_dimmer_vitrinekast", "30")
                if items.switch_led_strip_tv_toggle != ON:
                    events.sendCommand("switch_led_strip_tv_toggle", "ON")
                if items.switch_groene_tl_toggle != ON:
                    events.sendCommand("switch_groene_tl_toggle", "ON")

            elif "switch_scene_living_full" in trigger or scene_number == "3":
                if items.number_scene_lights_living != 3:
                    events.postUpdate("number_scene_lights_living", "3")

                # uitvoeren switch acties
                if str(items.number_scene_lights_living) != "3":
                    events.postUpdate("number_scene_lights_living", "3")
                if items.switch_scene_living_chill != OFF:
                    events.postUpdate("switch_scene_living_chill", "OFF")
                if items.switch_scene_living_full != ON:
                    events.postUpdate("switch_scene_living_full", "ON")

                # uitvoeren device acties
                if str(items.light_woonkamer_dimmer_boekenkast) != "100":
                    events.sendCommand("light_woonkamer_dimmer_boekenkast", "100")
                if str(items.light_woonkamer_dimmer_vitrinekast) != "100":
                    events.sendCommand("light_woonkamer_dimmer_vitrinekast", "100")
                if items.switch_led_strip_tv_toggle != OFF:
                    events.sendCommand("switch_led_strip_tv_toggle", "OFF")
                if items.switch_groene_tl_toggle != OFF:
                    events.sendCommand("switch_groene_tl_toggle", "OFF")

            elif scene_number == "4":
                    if str(items.number_scene_lights_living) != "4":
                        events.postUpdate("number_scene_lights_living", "4")
                    if items.switch_scene_living_chill != OFF:
                        events.postUpdate("switch_scene_living_chill", "OFF")
                    if items.switch_scene_living_full != OFF:
                        events.postUpdate("switch_scene_living_full", "OFF")

                # # output variables
                # logging.info("**** output scene states:")
                # logging.info("output number_scene_lights_living: " + str(items.number_scene_lights_living))
                # logging.info("output switch_scene_living_chill: " + str(items.switch_scene_living_chill))
                # logging.info("output switch_scene_living_full: " + str(items.switch_scene_living_full))

automationManager.addRule(rule_scene_lights_living())	


############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################

# class rule_scene_lights_kitchen (SimpleRule):
#     def __init__(self):
#         self.triggers = [ 
#                             StartupTrigger(), 
                            
#                             ItemCommandTrigger("timer_rule_scene_kitchen_new_init_hardware", command="OFF"),

#                             #ItemStateChangeTrigger("light_keuken_dimmer_plafond"),
#                             #ItemStateChangeTrigger("light_woonkamer_dimmer_vitrinekast"),
#                             ItemStateChangeTrigger("light_eettafel_toggle", state="ON",previousState="OFF"),
#                             ItemStateChangeTrigger("light_eettafel_toggle", state="ON",previousState="OFF"),

#                             ItemCommandTrigger("number_scene_lights_kitchen"),
#                             ItemCommandTrigger("switch_scene_living_off"),
#                             ItemCommandTrigger("switch_scene_living_cooking"),
#                             ItemCommandTrigger("switch_scene_living_dining")
#                             ItemCommandTrigger("switch_scene_living_full")
#                         ]

#     def execute(self, module, input):
#         #logging.info("STARTED")


#         ######################################################################################
#         # initialize programmable items
#         if str(items.timer_rule_scene_woonkamer_new_init_hardware) == "NULL":
#             events.postUpdate("timer_rule_scene_woonkamer_new_init_hardware","OFF")    
#         #if str(items.timer_rule_scene_woonkamer_disable_detection) == "NULL":
#             #events.postUpdate("timer_rule_scene_woonkamer_disable_detection","OFF")  

#         # check if devices are null...
#         if str(items.light_woonkamer_dimmer_boekenkast) == "NULL" or str(items.light_woonkamer_dimmer_vitrinekast) == "NULL" or str(items.switch_led_strip_tv_toggle) == "NULL" or str(items.switch_groene_tl_toggle) == "NULL":
#             if str(items.light_woonkamer_dimmer_boekenkast) == "NULL":
#                 logging.info("Dimmer boekenkast is in unknown state, pending refresh")
#             if str(items.light_woonkamer_dimmer_vitrinekast) == "NULL":
#                 logging.info("Dimmer vitrinekast is in unknown state, pending refresh")
#             if str(items.switch_led_strip_tv_toggle) == "NULL":
#                 logging.info("Led strip TV is in unknown state, polling MQTT")
#                 Mqtt.publish("mosquitto", "cmnd/" +" sonoff_switch_ledstrip_tv" + "/status", "0")
#             if str(items.switch_groene_tl_toggle) == "NULL":
#                 logging.info("Groene TL is in unknown state, polling MQTT")
#                 Mqtt.publish("mosquitto", "cmnd/" +" sonoff_green_tl" + "/status", "0")
                        
#             # Reschedule in 30 seconds until the items are in a proper state, if timer is somehow not yet running
#             if items.timer_rule_scene_woonkamer_new_init_hardware != ON:
#                 events.sendCommand("timer_rule_scene_woonkamer_new_init_hardware","ON")
#         #######################################################################################
#         else:           
#             # set scene number to scene and execute commands
#             scene_number = ""
#             if "event" in input:
#                 trigger = str(input['event'])
#                 if "number_scene_lights_living" in trigger:
#                     scene_number = str(input['command'])
#                     #logging.info("Recieved command from GUI(" + str(scene_number) + ")") 
#                     #logging.info("1 timer_rule_scene_woonkamer_new_gui_set_new_scene: " + str(items.timer_rule_scene_woonkamer_new_gui_set_new_scene))
#                     #events.sendCommand("timer_rule_scene_woonkamer_disable_detection", "ON")
#                 #else:
#                     #logging.info("2 timer_rule_scene_woonkamer_new_gui_set_new_scene: " + str(items.timer_rule_scene_woonkamer_new_gui_set_new_scene))
#                     #if items.timer_rule_scene_woonkamer_new_gui_set_new_scene == ON:
#                         #logging.info("timer is running, quitting script")
#             else:
#                 trigger = "startup"
            
#             #######################################################################################
#             #logging.info(trigger)
#             # # device states
#             # logging.info("**** input Device states:")
#             # logging.info("input light_woonkamer_dimmer_boekenkast: " + str(items.light_woonkamer_dimmer_boekenkast))
#             # logging.info("input light_woonkamer_dimmer_vitrinekast: " + str(items.light_woonkamer_dimmer_vitrinekast))
#             # logging.info("input switch_led_strip_tv_toggle: " + str(items.switch_led_strip_tv_toggle))
#             # logging.info("input switch_groene_tl_toggle: " + str(items.switch_groene_tl_toggle))

#             # # input variables
#             # logging.info("**** input scene states:")
#             # logging.info("input number_scene_lights_living: " + str(items.number_scene_lights_living))
#             # logging.info("input switch_scene_living_off: " + str(items.switch_scene_living_off))
#             # logging.info("input switch_scene_living_chill: " + str(items.switch_scene_living_chill))
#             # logging.info("input switch_scene_living_full: " + str(items.switch_scene_living_full))

            
#             # skip processing if number_scene_lights_living received command
#             #if items.timer_rule_scene_woonkamer_disable_detection == OFF:
#             if trigger == "startup":
#                 if str(items.light_woonkamer_dimmer_boekenkast) == "0" and str(items.light_woonkamer_dimmer_vitrinekast) == "0" and items.switch_led_strip_tv_toggle == OFF and items.switch_groene_tl_toggle == OFF:
#                     scene_number = "1"
#                 elif str(items.light_woonkamer_dimmer_boekenkast) == "30" and str(items.light_woonkamer_dimmer_vitrinekast) == "30" and items.switch_led_strip_tv_toggle == ON and items.switch_groene_tl_toggle == ON:
#                     scene_number = "2"
#                 elif str(items.light_woonkamer_dimmer_boekenkast) == "100" and str(items.light_woonkamer_dimmer_vitrinekast) == "100" and items.switch_led_strip_tv_toggle == OFF and items.switch_groene_tl_toggle == OFF:
#                     scene_number = "3"
#                 else:
#                     scene_number = "4"
#             #######################################################################################

#            #logging.info(scene_number)
#             #detect which event has triggered the rule)
#             if "switch_scene_living_off" in trigger or scene_number == "1":

#                 if items.number_scene_lights_living != 1:
#                     events.postUpdate("number_scene_lights_living", "1")
                
#                 # uitvoeren switch acties
#                 if items.switch_scene_living_off != ON:
#                     events.postUpdate("switch_scene_living_off",    "ON")
#                 if items.switch_scene_living_chill != OFF:
#                     events.postUpdate("switch_scene_living_chill",  "OFF")
#                 if items.switch_scene_living_full != OFF:    
#                     events.postUpdate("switch_scene_living_full",   "OFF")

#                 # uitvoeren device acties # status is net gedetecteerd, dus worden hier niet ingesteld, hoef niks te doen
#                 if (str(items.light_woonkamer_dimmer_boekenkast) != "0"):
#                     events.sendCommand("light_woonkamer_dimmer_boekenkast", "OFF")
#                 if (str(items.light_woonkamer_dimmer_vitrinekast) != "0"):
#                     events.sendCommand("light_woonkamer_dimmer_vitrinekast", "OFF")
#                 if items.switch_led_strip_tv_toggle != OFF:
#                     events.sendCommand("switch_led_strip_tv_toggle", "OFF")
#                 if items.switch_groene_tl_toggle != OFF:
#                     events.sendCommand("switch_groene_tl_toggle", "OFF")

#             elif "switch_scene_living_chill" in trigger or scene_number == "2":
#                 if items.number_scene_lights_living != 2:
#                     events.postUpdate("number_scene_lights_living", "2")
                
#                 # uitvoeren switch acties
#                 if items.switch_scene_living_off != OFF:
#                     events.postUpdate("switch_scene_living_off",    "OFF")
#                 if items.switch_scene_living_chill != ON:
#                     events.postUpdate("switch_scene_living_chill",  "ON")
#                 if items.switch_scene_living_full != OFF:
#                     events.postUpdate("switch_scene_living_full",   "OFF")
                
#                 # uitvoeren device acties
#                 if (str(items.light_woonkamer_dimmer_boekenkast) != "30"):
#                     #events.sendCommand("light_woonkamer_dimmer_boekenkast", "30")
#                     events.sendCommand("light_woonkamer_dimmer_boekenkast", "30")
#                 if (str(items.light_woonkamer_dimmer_vitrinekast) != "30"):
#                     events.sendCommand("light_woonkamer_dimmer_vitrinekast", "30")
#                 if items.switch_led_strip_tv_toggle != ON:
#                     events.sendCommand("switch_led_strip_tv_toggle", "ON")
#                 if items.switch_groene_tl_toggle != ON:
#                     events.sendCommand("switch_groene_tl_toggle", "ON")

#             elif "switch_scene_living_full" in trigger or scene_number == "3":
#                 if items.number_scene_lights_living != 3:
#                     events.postUpdate("number_scene_lights_living", "3")

#                 # uitvoeren switch acties
#                 if str(items.number_scene_lights_living) != "3":
#                     events.postUpdate("number_scene_lights_living", "3")
#                 if items.switch_scene_living_off != OFF:
#                     events.postUpdate("switch_scene_living_off", "OFF")
#                 if items.switch_scene_living_chill != OFF:
#                     events.postUpdate("switch_scene_living_chill", "OFF")
#                 if items.switch_scene_living_full != ON:
#                     events.postUpdate("switch_scene_living_full", "ON")

#                 # uitvoeren device acties
#                 if str(items.light_woonkamer_dimmer_boekenkast) != "100":
#                     events.sendCommand("light_woonkamer_dimmer_boekenkast", "100")
#                 if str(items.light_woonkamer_dimmer_vitrinekast) != "100":
#                     events.sendCommand("light_woonkamer_dimmer_vitrinekast", "100")
#                 if items.switch_led_strip_tv_toggle != OFF:
#                     events.sendCommand("switch_led_strip_tv_toggle", "OFF")
#                 if items.switch_groene_tl_toggle != OFF:
#                     events.sendCommand("switch_groene_tl_toggle", "OFF")

#             elif scene_number == "4":
#                     if str(items.number_scene_lights_living) != "4":
#                         events.postUpdate("number_scene_lights_living", "4")
#                     if items.switch_scene_living_off != OFF:
#                         events.postUpdate("switch_scene_living_off", "OFF")
#                     if items.switch_scene_living_chill != OFF:
#                         events.postUpdate("switch_scene_living_chill", "OFF")
#                     if items.switch_scene_living_full != OFF:
#                         events.postUpdate("switch_scene_living_full", "OFF")

#                 # # output variables
#                 # logging.info("**** output scene states:")
#                 # logging.info("output number_scene_lights_living: " + str(items.number_scene_lights_living))
#                 # logging.info("output switch_scene_living_off: " + str(items.switch_scene_living_off))
#                 # logging.info("output switch_scene_living_chill: " + str(items.switch_scene_living_chill))
#                 # logging.info("output switch_scene_living_full: " + str(items.switch_scene_living_full))

# automationManager.addRule(rule_scene_lights_living())	