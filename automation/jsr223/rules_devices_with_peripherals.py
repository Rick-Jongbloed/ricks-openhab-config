from openhab.log import logging
from openhab.triggers import item_triggered, ITEM_CHANGE

@item_triggered("spacecave_pc_fixed_net_online",ITEM_CHANGE)
def rule_spacecave_turn_monitors_on_when_pc_is_turned_on():
    logging.info("**** rule_spacecave_turn_monitors_on_when_pc_is_turned_on rule running due to state change")
    if items.spacecave_pc_fixed_net_online == ON and items.switch_monitor_versterker_toggle == OFF:
        logging.info("**** spacecave_pc_fixed_net_online is ON, switch_monitor_versterker_toggle is OFF, TURNING switch_monitor_versterker_toggle ON ****")
        events.sendCommand("switch_monitor_versterker_toggle", "ON")
    if items.spacecave_pc_fixed_net_online == OFF and items.switch_monitor_versterker_toggle == ON:
        logging.info("**** spacecave_pc_fixed_net_online is OFF, switch_monitor_versterker_toggle is ON, TURNING switch_monitor_versterker_toggle OFF ****")
        events.sendCommand("switch_monitor_versterker_toggle", "OFF")