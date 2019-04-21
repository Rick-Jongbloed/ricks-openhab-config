# trigger op:
# 1. flip switch test 1
# actie:
# zet switch 2
# zet switch 3
# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")

# from openhab.triggers import ChannelEventTrigger,item_triggered,ITEM_UPDATE, ItemCommandTrigger, ItemStateChangeTrigger
# from openhab.log import logging

# class rule_test_button_classes_definitions(SimpleRule):
#     def __init__(self):
#        # self.item_name = "test_switch"
#         self.triggers = [ 
#                             #ItemCommandTrigger(self.item_name, command="OFF")
#                             #ItemCommandTrigger(self.item_name)
#                             ItemStateChangeTrigger("test_switch")
#                         ]
#     # maak een uitleesmodule
#     def test_string_1(self, number):
#         self.test_string_1 = number
#         # logging.info(self.test_string_1) 
#         return self
    
#     def test_string_2(self):
#         self.test_string_2 = "2222BLAAT"
#         # logging.info(self.test_string_2)
#         return self

#     def execute(self, module, input):
#         logging.info(input)
#         s = rule_test_button_classes_definitions()
#         s.test_string_1(5)
#         s.test_string_2()
#         logging.info(s.test_string_1)
#         logging.info(s.test_string_2)
            
# automationManager.addRule(rule_test_button_classes_definitions())


# class Spam(object):

#     def order(self, number):
#         print "spam " * number

#     def order_eggs():
#         print " and eggs!"

#     s = Spam()
#     s.order(3)
#     order_eggs()


    



# class MyRule111(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ItemStateChangeTrigger("test_switch") ]
#     def execute(self, module, input):
#        logging.info("test")
#        logging.info(input)
#        logging.info(input.get("newState"))
#        logging.info(input.get("oldState"))
# automationManager.addRule(MyRule111())