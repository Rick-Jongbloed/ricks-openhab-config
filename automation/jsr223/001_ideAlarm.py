from lucid.rules import rule, addRule
from idealarm import ideAlarm
from lucid.utils import hasReloadFinished, getEvent, postUpdateCheckFirst, sendCommandCheckFirst
from lucid.triggers import ItemCommandTrigger
import lucid.config as config
from logging import DEBUG, INFO, WARNING, ERROR

@rule
class ideAlarmTrigger(object):

    """Make ideAlarm trigger on item changes"""
    def getEventTriggers(self):
        return ideAlarm.getTriggers()

    def execute(self, modules, inputs):
        if not hasReloadFinished(True): 
            return
        ideAlarm.execute(modules, inputs)

addRule(ideAlarmTrigger())

# # do stuff on keypad press
# #   create item that stores complete password (keypad: idealarm_keypad, full_key: idealarm_keypad_full)
# #   create rule to process keypresses:
# #       process keypresses
# #       use V to complete keypresses
# #       use X to reset keypresses


# Rule to test out keypad compatibility
@rule
class ideAlarmKeypad(object):

    """Make ideAlarm trigger on item changes"""
    def getEventTriggers(self):
        return [
            ItemCommandTrigger('idealarm_keypad'),
        ]

    def execute(self, modules, inputs):
        
        event = getEvent(inputs)
        key_pressed = str(event.state)
        entered_alarm_code = str(items.idealarm_keypad_full)
        current_alarm_status = str(items.Z1_Status)
        configured_alarm_code = config.idealarm['alarm_code']
        postUpdateCheckFirst('idealarm_keypad','')  # unselect item so the interface is snappy

        if key_pressed == "X":
            postUpdateCheckFirst('idealarm_keypad_full','')
        elif key_pressed == "V":
            if len(entered_alarm_code) > 0 and entered_alarm_code == configured_alarm_code:              

                self.log.info('Clearing alarm code')
                postUpdateCheckFirst('idealarm_keypad_full','')
                
                # toggle alarm - check status of alarm. If alarm = home:
                if current_alarm_status == "0": 
                    sendCommandCheckFirst('Toggle_Z1_Armed_Away','ON')
                elif current_alarm_status == "1":
                    sendCommandCheckFirst('Toggle_Z1_Armed_Home','ON')
                else:
                    sendCommandCheckFirst('Toggle_Z1_Armed_Away','ON')
            else:
                # security incident... have to define
                self.log.info('Code incorrect!')
                self.log.info('Clearing alarm code')
                postUpdateCheckFirst('idealarm_keypad_full','')
                # pushover bericht!
                pass
        else:
            new_entered_alarm_code = entered_alarm_code + key_pressed
            postUpdateCheckFirst('idealarm_keypad_full',new_entered_alarm_code)    
addRule(ideAlarmKeypad())