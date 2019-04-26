scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

#from openhab.triggers import ChannelEventTrigger,StartupTrigger
from openhab.triggers import ChannelEventTrigger
from lucid.triggers import StartupTrigger
from openhab.log import logging
import datetime

# VERWIJDEREN ALS DAG  -> NACHT WERKT!!!
# class rule_astro_day_turns_into_night(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ChannelEventTrigger(channelUID="Astro:sun:home:set#event", event="END") ]
#     def execute(self, module, input):
#         logging.info("Rule rule_astro_day_turns_into_night started...")
#         events.sendCommand("day" "ON")
#         events.sendCommand("night" "OFF")
# automationManager.addRule(rule_astro_day_turns_into_night())

# VERWIJDEREN ALS NACHT -> DAG WERKT!!!
# class rule_astro_night_turns_into_day(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ChannelEventTrigger(channelUID="astro:sun:home:rise#event", event="START") ]
#     def execute(self, module, input):
#         logging.info("Rule rule_astro_night_turns_into_day started...")
#         events.sendCommand("day" "OFF")
#         events.sendCommand("night" "ON")
# automationManager.addRule(rule_astro_night_turns_into_day())

class rule_astro_manage_day_or_night_switch(SimpleRule):
    def __init__(self):
                        self.triggers = [ 
                            StartupTrigger(),
                            ChannelEventTrigger(channelUID="astro:sun:home:rise#event", event="START"),
                            ChannelEventTrigger(channelUID="astro:sun:home:set#event", event="END")
                        ]
    def execute(self, module, input):
        now = datetime.datetime.now()
        if str(now) > str(items.sunrise_time) and str(now) < str(items.sunset_time):
            events.sendCommand("day" "ON")
            events.sendCommand("night" "OFF")
        elif str(now) > str(items.sunset_time) or str(now) < str(items.sunrise_time):
            events.sendCommand("day", "OFF")
            events.sendCommand("night", "ON")
        logging.info("Rule rule_astro_manage_day_or_night_switch started DAY='" + str(items.day) + "' NIGHT='" + str(items.night) + "'...")
automationManager.addRule(rule_astro_manage_day_or_night_switch())