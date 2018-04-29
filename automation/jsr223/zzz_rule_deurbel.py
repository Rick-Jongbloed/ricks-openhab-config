#https://community.openhab.org/t/configurable-scenarios/10140/3

scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")

from org.eclipse.smarthome.core.library.types import (HSBType, DecimalType, PercentType)
from openhab.triggers import ItemCommandTrigger
from openhab.log import logging
from openhab.actions import Pushover
import time # timer

import urllib # save camera file
#import requests

class rule_deurbel_pressed(SimpleRule):
    def __init__(self):
        # self.item_name = "switch_deurbel_toggle"
        self.item_name = "test_switch"
        self.group_settings = "settings_deurbel_action_selection"

        self.triggers = [ ItemCommandTrigger(self.item_name) ]
        
    # maak een uitleesmodule
    # def initialize_devices(self):
        # 1. initialiseer alle devices
        # als er een device niet beschikbaar is, reschedule dan deze rule/

        # self.test_string_1 = number
        # logging.info(self.test_string_1) 
        # return self
    
    def read_settings(self):
        group = itemRegistry.getItem(self.group_settings)
        self.items_enabled = []
        for item_setting in group.getAllMembers():
            if str(item_setting.state) == "ON":
                substring_setting           = "deurbel_setting_"
                if item_setting.name.startswith(substring_setting):
                    item_actuator_name = item_setting.name[len(substring_setting):]
                    if item_actuator_name in items:
                        self.items_enabled.append(item_actuator_name)
                    else:
                        logging.info("!!! Item '" + item_actuator_name + "' doesn't exist! - Not processsing item yet") # should be send to whatapp / pushover
        return self
        # reads settings from openhab (group settings_deurbel_action_selection)
        # the item name of the action switch is in the name?
        # bel deurbel
        # bel alexa
        # bel mihome gateway
        # lichtsignaal woonkamer
        # ooit voor elke setting een eigen init maken, goed structureren
        # self.test_string_2 = "2222BLAAT"
        # logging.info(self.test_string_2)

    def execute(self, module, input):
        s = rule_deurbel_pressed()
        s.read_settings()
        logging.info(s.items_enabled)
        # s.test_string_1(5)
        # s.test_string_2()
        # logging.info(s.test_string_1)
        # logging.info(s.test_string_2)
            
automationManager.addRule(rule_deurbel_pressed())



# # all actions:
class rule_toggle_notification_light_eettafel(SimpleRule):
    def __init__(self):
        self.item_name_actuator = "light_eettafel_color"
        self.item_name_notification = "toggle_notification_light_eettafel"

        self.triggers = [ ItemCommandTrigger(self.item_name_notification, command="ON") ]

        

    def execute(self, module, input):
   
        self.hue = DecimalType(0)
        self.sat = PercentType(100)
        self.bright = PercentType(100)

        # for count in range(0, 100, 5):
        #     #self.hue = DecimalType(count)
        #     self.bright = PercentType(count)
        #     self.light = HSBType(self.hue,self.sat,self.bright)
        #     events.sendCommand(self.item_name_actuator, str(self.light))
        #     time.sleep(1)
        # for count in reversed(range(0, 100, 5)):
        #     #self.hue = DecimalType(count)
        #     self.bright = PercentType(count)
        #     self.light = HSBType(self.hue,self.sat,self.bright)
        #     events.sendCommand(self.item_name_actuator, str(self.light))
        #     #self.hue = self.hue +=1
        #     time.sleep(0.3)
        
        for count in range(0, 10, 1):
            if count % 2 == 0:
                self.bright = PercentType(0)
            else:
                self.bright = PercentType(100)
            self.light = HSBType(self.hue,self.sat,self.bright)

            events.sendCommand(self.item_name_actuator, str(self.light))
            time.sleep (2)
        events.sendCommand(self.item_name_actuator, "OFF")
        events.postUpdate(self.item_name_notification, "OFF")
        
automationManager.addRule(rule_toggle_notification_light_eettafel())

class rule_toggle_notification_sound_alexa(SimpleRule):
    def __init__(self):
        self.item_name = "toggle_notification_sound_alexa"
        self.alarm_sound = "ECHO:system_alerts_melodic_01"
        self.alexa_alarm_item = "amazon_echo_dot_play_alarm_sound" 
        
        self.triggers = [
                            ItemCommandTrigger(self.item_name, command="ON"),
                            ItemCommandTrigger(self.item_name, command="OFF") 
                        ]    
        
    def execute(self, module, input):
        input_command = input['command']
        #logging.info(input_command)
        if input['command'] == "ON":
            logging.info(self.alexa_alarm_item)
            logging.info(self.alarm_sound)
            events.sendCommand(self.alexa_alarm_item, self.alarm_sound)
        else:
            events.sendCommand(self.alexa_alarm_item, "")

automationManager.addRule(rule_toggle_notification_sound_alexa())


class rule_toggle_notification_message_pushover(SimpleRule):
    def __init__(self):
        self.item_name = "toggle_notification_message_pushover"        
        self.triggers = [ ItemCommandTrigger(self.item_name, command="ON") ]
        #self.triggers = [ ItemCommandTrigger("toggle_notification_message_pushover") ]
        remote_url = "http://192.168.1.25:88/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr=rick&pwd=eY8aQArrk9QU"
        local_file = "/tmp/local-filename.jpg"
        logging.info("TEST1")
        
    def execute(self, module, input):
        logging.info("TEST2")
        Pushover.pushover("TEEEESSSST!!!!", "Telefoon_prive_rick01")  
        
        urllib.urlretrieve("http://192.168.1.25:88/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr=rick&pwd=eY8aQArrk9QU", "camera.jpg")
        logging.info("TEST3")
        #urllib.urlretrieve(url, local_file)
        Pushover.sendPushoverImage("Er is aangebeld", "camera.jpg")
        #Pushover.sendPushoverImage(“Hello, this is a message with attached image.”, “/path/to/image.jpeg”);
automationManager.addRule(rule_toggle_notification_message_pushover())


