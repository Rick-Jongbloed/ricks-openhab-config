from core.triggers import when
from core.rules import rule
from core.actions import Pushover
from core.log import logging, LOG_PREFIX

@rule("Rule bedroom buttons")
@when("Channel mihome:sensor_switch:158d00016c0af6:button triggered SHORT_PRESSED")
@when("Channel mihome:sensor_switch:158d00016c0af6:button triggered DOUBLE_PRESSED")
@when("Channel mihome:sensor_switch:158d00016c0af6:button triggered LONG_PRESSED")
@when("Channel mihome:sensor_switch:158d00016c0af6:button triggered LONG_RELEASED")
@when("Channel mihome:sensor_switch:158d000210bee8:button triggered SHORT_PRESSED")
@when("Channel mihome:sensor_switch:158d000210bee8:button triggered DOUBLE_PRESSED")
@when("Channel mihome:sensor_switch:158d000210bee8:button triggered LONG_PRESSED")
@when("Channel mihome:sensor_switch:158d000210bee8:button triggered LONG_RELEASED")
def rule_bedroom_buttons(event):
    function = 'rules.bedroom_buttons'
    log = logging.getLogger(LOG_PREFIX + '.' + function)

    #double check as i'm using two switches
    #triggered_event = str(input['event']).replace(self.device_1 + " triggered ", "")
    #triggered_event = triggered_event.replace(self.device_2 + " triggered ", "")
    triggered_event = str(event).replace("mihome:sensor_switch:158d00016c0af6:button" + " triggered ", "")
    triggered_event = triggered_event.replace("mihome:sensor_switch:158d000210bee8:button" + " triggered ", "")
    log.info("SWITCH INGEDRUKT: " + triggered_event)

    # load light settings
    mood_light_dimmer = str(items.light_plafond_slaapkamer_dimmer_setting_mood_light)
    mood_light_colortemp = str(items.light_plafond_slaapkamer_colortemp_setting_mood_light)
    full_light_dimmer = str(items.light_plafond_slaapkamer_dimmer_setting_full_light)
    full_light_colortemp = str(items.light_plafond_slaapkamer_colortemp_setting_full_light)

    # set light type # BUG HERE!!!! INIT NEEDED TO SET THESE IF NULL, OR USE CONFIG FIRST AND LOG A WARNING ABOUT THIS
    if not(mood_light_dimmer or mood_light_colortemp or full_light_dimmer or full_light_colortemp):
        log.warn("Settings have not been set. See instellingen -> Licht slaapkamer - mood/full")
    else:
        if str(items.light_plafond_slaapkamer_toggle) == "ON":
            if str(items.light_plafond_slaapkamer_dimmer) == mood_light_dimmer and str(items.light_plafond_slaapkamer_colortemp) == mood_light_colortemp:
                light_configuration = "mood_light"
            elif str(items.light_plafond_slaapkamer_dimmer) == full_light_dimmer and str(items.light_plafond_slaapkamer_colortemp) == full_light_colortemp:
                light_configuration = "full_light"
            else:
                light_configuration = "unknown"


        if triggered_event == "SHORT_PRESSED":
            if items.rule_xiaomi_switch_slaapkamer_all_off_timer == ON:
                log.info("*** Timer cancelled...")    
                events.postUpdate("rule_xiaomi_switch_slaapkamer_all_off_timer", "OFF")
                Pushover.pushover("All off timer cancelled...", "Telefoon_prive_rick01")
            else:
                log.info("!!! Timer not running..., using regular function")
                # toggle bedroom light (sfeerlicht)
                log.info("!!! items.light_plafond_slaapkamer_toggle: " + str(items.light_plafond_slaapkamer_toggle))
                if str(items.light_plafond_slaapkamer_toggle) == "ON":
                    # if light_configuration != "mood_light":       # Disabled as it's not practical. Mood light is set when we go to bed. We expect the light to turn off when you click once
                    #     events.sendCommand("light_plafond_slaapkamer_dimmer",mood_light_dimmer)
                    #     events.sendCommand("light_plafond_slaapkamer_colortemp",mood_light_colortemp)
                    # else:
                        events.sendCommand("light_plafond_slaapkamer_toggle","OFF")

                if str(items.light_plafond_slaapkamer_toggle) == "OFF":
                    log.info("Light is off, ")
                    log.info("Turning dimmer to mood light dimmer: " + mood_light_dimmer)
                    log.info("Turning dimmer to mood light dimmer: " + mood_light_colortemp)
                    events.sendCommand("light_plafond_slaapkamer_dimmer",mood_light_dimmer)
                    events.sendCommand("light_plafond_slaapkamer_colortemp",mood_light_colortemp)
                    events.postUpdate("light_plafond_slaapkamer_toggle","ON") 
    #               Pushover.pushover("All off timer not running...", "Telefoon_prive_rick01")
                
        elif triggered_event == "DOUBLE_PRESSED":
            # toggle bedroom light (FULL)
            if str(items.light_plafond_slaapkamer_toggle) == "ON":
                if light_configuration != "full_light":
                    events.sendCommand("light_plafond_slaapkamer_dimmer",full_light_dimmer)
                    events.sendCommand("light_plafond_slaapkamer_colortemp",full_light_colortemp)
                else:
                    events.sendCommand("light_plafond_slaapkamer_toggle","OFF")

            if str(items.light_plafond_slaapkamer_toggle) == "OFF":
                events.sendCommand("light_plafond_slaapkamer_dimmer",full_light_dimmer)
                events.sendCommand("light_plafond_slaapkamer_colortemp",full_light_colortemp)
                events.postUpdate("light_plafond_slaapkamer_toggle","ON") 

        elif triggered_event == "LONG_PRESSED":
            # check if items.rule_xiaomi_switch_slaapkamer_all_off_timer is OFF (or NULL)
            if items.rule_xiaomi_switch_slaapkamer_all_off_timer != ON:
                events.sendCommand("rule_xiaomi_switch_slaapkamer_all_off_timer", "ON")
                Pushover.pushover("ALLES UIT KNOP: Timer gestart", "Telefoon_prive_rick01")
                log.info("*** All off timer started (60 seconds)")
            else:
                log.info("*** All off timer is already running (<60 seconds)")
                Pushover.pushover("All off timer is already running...", "Telefoon_prive_rick01")

        elif triggered_event == "LONG_RELEASED":
            pass