# from openhab.rules import rule, addRule
# from idealarm import ideAlarm #######
# from mylib.utils import hasReloadFinished

# @rule
# class ideAlarmTrigger(object):

#     """Make ideAlarm trigger on item changes"""
#     def getEventTriggers(self):
#         return ideAlarm.getTriggers()

#     def execute(self, modules, inputs):
#         if not hasReloadFinished(True): return
#         ideAlarm.execute(modules, inputs)

# addRule(ideAlarmTrigger())

# # do stuff on keypad press
# #   create item that stores complete password (keypad: idealarm_keypad, full_key: idealarm_keypad_full)
# #   create rule to process keypresses:
# #       process keypresses
# #       use V to complete keypresses
# #       use X to reset keypresses

# class rule_alarm_keypad_process(SimpleRule):
#     def __init__(self):
#         self.triggers = [ 
#                             #StartupTrigger(),                                                               # Run on startup to initialize, will reset the timer(!)
#                             ItemStateChangeTrigger("idealarm_keypad")                          
#                         ]
#     def execute(self, module, input):
    
# # automationManager.addRule(rule_alarm_keypad_process())