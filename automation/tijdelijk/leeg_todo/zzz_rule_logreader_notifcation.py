# # scriptExtension.importPreset("RuleSimple")
# # scriptExtension.importPreset("RuleSupport")

# from core.triggers import when #item_triggered, ITEM_CHANGE
# from core.log import logging
# from core.actions import Things, Pushover
# from core.rules import rule

# #@item_triggered("logreader_last_read", ITEM_CHANGE)
# @rule("Logreader processing rule to pushover")
# @when("Item logreader_last_read changed")
# def rule_logreader_last_read_notification_on_error():
#     logging.info("rule rule_logreader_last_read_notification_on_error starts")
#     logging.info(items.logreaderErrors.state)
#     logging.info(items.logreaderErrors)
#     if items.logreaderErrors.state > 0:
#          Pushover.pushover("LogReader alarm!" + str(items.logreaderErrors.state) + " Errors in log! Heres the last one:\n\n" + str(logreaderLastErrorLine.state), "Telefoon_prive_rick01")