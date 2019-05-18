# from core.triggers import when
# from core.rules import rule
# from core.actions import Pushover
# from core.log import logging, LOG_PREFIX

# @Rule("All off rule execute")
# @when("Item rule_xiaomi_switch_slaapkamer_all_off_timer received command OFF")
# def rule_all_off_execute(event):
#     function = 'rules.all_off_execute'
#     log = logging.getLogger(LOG_PREFIX + '.' + function)
#     log.info("rule_all_off_execute running.....")
        
#     group = itemRegistry.getItem("settings_all_off_selection")
#     for item_setting in group.getAllMembers():
#         # get corresponding setting
#         if str(item_setting.state) == "ON":
#             log.info("*** Processing setting item: '" + item_setting.name + "'")
#             substring_setting           = "_setting_all_off"
#             substring_actuator          = "_toggle"
#             #substring_actuator_computer = "_turn_off"       # hoe maak ik een toggle
#             # validate item_setting, should contain substring
#             if item_setting.name.endswith(substring_setting):
#                 item_actuator_name = item_setting.name[:-len(substring_setting)] + substring_actuator
#                 #validate if item_actuator exists
#                 if item_actuator_name in items:
#                     item_actuator_state = items[item_actuator_name]
#                         if item_actuator_state != OFF:
#                             log.info("*** Item'" + item_actuator_name + "' is '" + str(item_actuator_state) + "', turning item OFF")
#                             #events.sendCommand(item_actuator_name,"OFF")
#                         else:
#                             log.info("!!! Item'" + item_actuator_name + "' is '" + str(item_actuator_state) + "', NOT TURNING ITEM OFF")
#                             pass
#                     else:
#                         log.info("!!! Item '" + item_actuator_name + "' doesn't exist! - Not processsing item yet") # should be send to whatapp / pushover
#                 else:
#                     # log error / pushover (v2)
#                     pass
#         Pushover.pushover("ALLES UIT KNOP: Uitgevoerd", "Telefoon_prive_rick01")