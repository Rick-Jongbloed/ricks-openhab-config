from lucid.rules import rule, addRule
from lucid.triggers import ChannelEventTrigger, item_triggered, ITEM_UPDATE, ItemCommandTrigger
from lucid.actions import Pushover
from lucid.utils import hasReloadFinished, postUpdateCheckFirst, sendCommandCheckFirst
import lucid.config as config

@rule
class rule_xiaomi_switch_keuken(object):
    def getEventTriggers(self):
        device_1 = config.button_config['kitchen']['device_1']
        return [
             ChannelEventTrigger(channelUID=device_1, event="SHORT_PRESSED"),
             ChannelEventTrigger(channelUID=device_1, event="DOUBLE_PRESSED"),
             ChannelEventTrigger(channelUID=device_1, event="LONG_PRESSED"),
             ChannelEventTrigger(channelUID=device_1, event="LONG_RELEASED")
        ]

    def execute(self, modules, inputs):
        device_1 = config.button_config['kitchen']['device_1']
        
        triggered_event = str(inputs['event']).replace(device_1 + " triggered ", "")
        self.log.info("SWITCH PRESSED: " + triggered_event)

        if triggered_event == "SHORT_PRESSED":
            # if light = ON, turn light OFF
            # if light = OFF, turn light ON
            # if items.rule_xiaomi_switch_slaapkamer_all_off_timer == ON:
            #     logging.info("*** Timer cancelled...")    
            #     events.postUpdate("rule_xiaomi_switch_slaapkamer_all_off_timer", "OFF")
            #     Pushover.pushover("All off timer cancelled...", "Telefoon_prive_rick01")
            # else:
                # toggle bedroom light
                
                # logging.info("!!! Timer not running...")
                #Pushover.pushover("All off timer not running...", "Telefoon_prive_rick01")
            pass                
        elif triggered_event == "DOUBLE_PRESSED":
            # toggle different lamp styles (like hue, sfeer, bright, etc)

            
            pass

        elif triggered_event == "LONG_PRESSED":
            # turn ventiliation on
            events.sendCommand("number_ventilator_level_set_manual",3)
            # sendcommand, should always send
            # check if items.rule_xiaomi_switch_slaapkamer_all_off_timer is OFF (or NULL)
            #if items.rule_xiaomi_switch_kantoor_all_off_timer != ON:
                # events.sendCommand("rule_xiaomi_switch_slaapkamer_all_off_timer", "ON")
                # Pushover.pushover("ALLES UIT KNOP: Timer gestart", "Telefoon_prive_rick01")
                # logging.info("*** All off timer started (60 seconds)")
        #        pass
            #else:
                # logging.info("*** All off timer is already running (<60 seconds)")
                # Pushover.pushover("All off timer is already running...", "Telefoon_prive_rick01")
            pass
        elif triggered_event == "LONG_RELEASED":
            pass
            

addRule(rule_xiaomi_switch_keuken())