scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.triggers import item_triggered, ITEM_CHANGE
from openhab.log import logging
from openhab.actions import Mqtt, Pushover

@item_triggered("logreader_last_read", ITEM_CHANGE)
def rule_logreader_last_read_notification_on_error():
    logging.info("rule rule_logreader_last_read_notification_on_error starts")
    logging.info(items.logreaderErrors.state)
    logging.info(items.logreaderErrors)
    if items.logreaderErrors.state > 0:
         Pushover.pushover("LogReader alarm!" + str(items.logreaderErrors.state) + " Errors in log! Heres the last one:\n\n" + str(logreaderLastErrorLine.state), "Telefoon_prive_rick01")