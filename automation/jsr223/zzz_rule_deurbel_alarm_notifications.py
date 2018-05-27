#https://community.openhab.org/t/configurable-scenarios/10140/3

scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")

from org.eclipse.smarthome.core.library.types import (HSBType, DecimalType, PercentType)
from openhab.triggers import ItemCommandTrigger, StartupTrigger, ItemStateUpdateTrigger, item_triggered, ITEM_UPDATE
from openhab.log import logging
from openhab.actions import Pushover, Mqtt
from subprocess import call

import time         # timer
import os
import urllib       # save camera file

# Rule needed to make sure the status can be stored correctly
@item_triggered("switch_deurbel_switch_mode_1_mqtt", event_types=ITEM_UPDATE, result_item_name="switch_deurbel_switch_mode_1")
def rule_switch_deurbel_switch_mode_1_mqtt_changed():
	item_state = str(items.switch_deurbel_switch_mode_1_mqtt)
	if item_state == "NULL" or len(item_state) == 0:
		item_state = str(items.switch_deurbel_switch_mode_1)
	return item_state

# Rule needed to make sure the status can be stored correctly
@item_triggered("switch_deurbel_switch_topic_mqtt", event_types=ITEM_UPDATE, result_item_name="switch_deurbel_switch_topic")
def rule_switch_deurbel_switch_topic_mqtt_changed():
	item_state = str(items.switch_deurbel_switch_topic_mqtt)
	if item_state == "NULL" or len(item_state) == 0:
		item_state = str(items.switch_deurbel_switch_topic)
	return item_state


class rule_deurbel_pressed(SimpleRule):
	def __init__(self):
		# self.item_name = "switch_deurbel_toggle"
		self.item_name = "test_switch"
		self.group_settings = "settings_deurbel_action_selection"

		self.triggers = [
							StartupTrigger(),
							ItemCommandTrigger(self.item_name),
							
							# should add all settings related stuff (only setcommand) - not needed as it's only an output and no external configuration is needed
							ItemCommandTrigger("deurbel_setting_toggle_notification_sound_bel"),
							ItemCommandTrigger("timer_rule_deurbel_init_hardware", command="OFF"),
							ItemStateUpdateTrigger("switch_deurbel_button_toggle")
						]

	# debug (log) module
	def log_device_states(self):							# OK, works
	    logging.info("*************************************************************")
	    logging.info("switch_deurbel_button_toggle: " + str(items.switch_deurbel_button_toggle))
	    logging.info("switch_deurbel_led_power: " + str(items.switch_deurbel_led_power))
	    logging.info("switch_deurbel_led_state: " + str(items.switch_deurbel_led_state))
	    logging.info("switch_deurbel_button_topic: " + str(items.switch_deurbel_button_topic))
	    logging.info("switch_deurbel_switch_mode_1: " + str(items.switch_deurbel_switch_mode_1))
	    logging.info("switch_deurbel_switch_topic: " + str(items.switch_deurbel_switch_topic))
	    logging.info("deurbel_setting_toggle_notification_sound_bel: " + str(items.deurbel_setting_toggle_notification_sound_bel))
	    logging.info("*************************************************************")
	 
	def initialize_devices(self):							# OK, works, but could use a rewrite
		# This function should only make sure all devices are populated with the current values. Setting the devices to the correct values happens later

		# initialize button (so it doesn't show in the uninit list) 
		if str(items.switch_deurbel_button_toggle) == "NULL":						
			events.postUpdate("switch_deurbel_button_toggle","UNSET")

		#initialize pollable items
		if str(items.switch_deurbel_button_topic) != "sonoff_deurbel_button" or \
			str(items.switch_deurbel_toggle) == "NULL" or \
			str(items.switch_deurbel_led_state) == "NULL" or \
			str(items.switch_deurbel_led_power) == "NULL" or \
			str(items.switch_deurbel_switch_mode_1) == "NULL" or \
			str(items.switch_deurbel_switch_topic) == "NULL" or \
			str(items.deurbel_setting_toggle_notification_sound_bel) == "NULL":

			logging.info("NULL states found: Starting initialization")
			self.initialized = False
			
			# initialize button topic (set button topic to 'sonoff_deurbel_button')
			if str(items.switch_deurbel_button_topic) != "sonoff_deurbel_button":
				Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_deurbel/ButtonTopic", "sonoff_deurbel_button")

			# Initialize switch mode 1
			if str(items.switch_deurbel_switch_mode_1) == "NULL":
				logging.info("Switch deurbel: switch_deurbel_switch_mode_1 is in an unknown state, pending refresh")
				Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_deurbel" + "/SwitchMode1", "")

			# Initialize switch topic
			if str(items.switch_deurbel_switch_topic) == "NULL":									# Executing mosquitto_pub as it's not possible to send an empty payload with the Openhab2 binding.  (option -n)
				logging.info("Switch deurbel: switch_deurbel_switch_topic is in an unknown state, pending refresh")
				command = "/usr/bin/mosquitto_pub -h 192.168.1.201 -t cmnd/sonoff_switch_deurbel/SwitchTopic -n"
				call(command, shell=True)
						
			# initialize led power item by querying led state (0=OFF, 8=ON) - DIT STUKJE KAN BETER!!
			if str(items.switch_deurbel_led_power) == "NULL":
				#logging.info("Led power of switch deurbel is in unknown state, pending refresh")
				if str(items.switch_deurbel_led_state) == "0":
					events.postUpdate("switch_deurbel_led_power","OFF")
					logging.info("POSTUPDATING LED POWER TO OFF")
				elif str(items.switch_deurbel_led_state) == "8":
					logging.info("POSTUPDATING LED POWER TO ON")
					events.postUpdate("switch_deurbel_led_power","ON")
				else:
					logging.info("UNKNOWN LED STATE. UNABLE TO SET LEDPOWER (LED state: " + str(items.switch_deurbel_led_state))
			
			# Reschedule in 30 seconds until the items are in a proper state, if timer is somehow not yet running
			if items.timer_rule_deurbel_init_hardware != ON:
				logging.info("Setting refresh timer (30s) & And updating MQTT Status")
				Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_deurbel" + "/status", "0")
				events.sendCommand("timer_rule_deurbel_init_hardware","ON")	
			else:
				logging.info("Not scheduling inittimer because it is already set (<30s): " + str(items.timer_rule_deurbel_init_hardware))
				
		else:
			self.initialized = True
		
		logging.info ("self.initialized: " + str(self.initialized))
		return self

	def read_settings(self):								# OK, works...
		group = itemRegistry.getItem(self.group_settings)
		self.items_enabled = []
		for item_setting in group.getAllMembers():					# could create a filter so the next line isn't needed.
			if str(item_setting.state) == "ON":
				substring_setting = "deurbel_setting_"
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

	def get_trigger_info(self,input):						# OK, works
		if "event" in input:
			self.trigger = str(input['event'])
		else:
			self.trigger = "startup"
		return self

	def door_bell_set(self):								# OK, works
		if str(items.switch_deurbel_switch_mode_1) != self.doorbell_switch_mode_1:
			logging.info("SETTING SwitchMode1 to " + self.doorbell_switch_mode_1)
			Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_deurbel/SwitchMode1", self.doorbell_switch_mode_1)

		if str(items.switch_deurbel_switch_topic) != self.doorbell_switch_topic:
			logging.info("SETTING SwitchTopic to " + self.doorbell_switch_topic + " (items.switch_deurbel_switch_topic: " + str(items.switch_deurbel_switch_topic) + ")")
			Mqtt.publish("mosquitto", "cmnd/" + "sonoff_switch_deurbel/SwitchTopic", self.doorbell_switch_topic)						

		if str(items.switch_deurbel_led_power) != self.doorbell_led_power:
			logging.info("SETTING led_power to " + self.doorbell_led_power)
			events.sendCommand("switch_deurbel_led_power",self.doorbell_led_power)						

		if str(items.deurbel_setting_toggle_notification_sound_bel) != self.doorbell_setting:
			logging.info("SETTING deurbel_setting_toggle_notification_sound_bel to " + self.doorbell_setting)
			events.postUpdate("deurbel_setting_toggle_notification_sound_bel", self.doorbell_setting)
		return self

	def door_bell_configure(self):							# OK, works
		if ("switch_deurbel_button_toggle" in self.trigger and str(items.deurbel_setting_toggle_notification_sound_bel) == "ON") or (not "switch_deurbel_button_toggle" in self.trigger and str(items.deurbel_setting_toggle_notification_sound_bel) == "OFF"):
			# DISABLE DOORBELL
			self.doorbell_setting = "OFF"
			self.doorbell_switch_mode_1 = "2"		
			self.doorbell_switch_topic = "sonoff_switch_deurbel_losgekoppeld"
			self.doorbell_led_power = "ON"
		else:
			# ENABLE DOORBELL 
			self.doorbell_setting = "ON"
			self.doorbell_switch_mode_1 = "2"
			self.doorbell_switch_topic = "sonoff_switch_deurbel"
			self.doorbell_led_power = "OFF"			
		return self

	def execute(self, module, input):
		s = rule_deurbel_pressed()							# defines object (still learning)
		s.read_settings()									# returns self.items_enabled
#		s.log_device_states()								# logs debug info
		s.get_trigger_info(input)							# returns self.trigger
		s.initialize_devices()								# set all devices to the current state if a device is NULL
		
		logging.info ("s.initialized: " + str(s.initialized))
		# if s.initialize_devices().initialized:
		if s.initialized:
			logging.info("initialized")
			s.door_bell_configure()
			s.door_bell_set()
		else:
			logging.info("not yet initialized")
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
		self.remote_url = "http://192.168.1.25:88/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr=rick&pwd=eY8aQArrk9QU"
		self.local_file = "camera.jpg"
		self.msg = "Er is aangebeld"

	def execute(self, module, input):
		urllib.urlretrieve(self.remote_url, self.local_file)
		Pushover.sendPushoverMessage(Pushover.pushoverBuilder(self.msg).withAttachment(self.local_file))
		os.remove(self.local_file)
		events.postUpdate(self.item_name,"OFF")
automationManager.addRule(rule_toggle_notification_message_pushover())


class rule_toggle_notification_message_pushover_alarm(SimpleRule):
	def __init__(self):
		self.item_name = "toggle_notification_message_pushover_alarm"
		self.triggers = [ ItemCommandTrigger(self.item_name, command="ON") ]
		self.msg = "ALARM gaat af!!"

	def execute(self, module, input):
		Pushover.sendPushoverMessage(Pushover.pushoverBuilder(self.msg))
		events.postUpdate(self.item_name,"OFF")
automationManager.addRule(rule_toggle_notification_message_pushover_alarm())

