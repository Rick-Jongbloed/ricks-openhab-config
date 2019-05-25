from core.rules import rule
from core.log import logging, LOG_PREFIX
from core.triggers import when

@rule("RFXCOM Remote 3, button A1 & A2")
@when("Item remote_3_a_1_command_id received update")
@when("Item remote_3_a_2_command_id received update")
def rule_remote_3_a_command_id_updated(event):
    function = 'remote_control.3.a'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("Rule rule_remote_3_a_command_id_updated running...")
    events.sendCommand("light_keuken_dimmer_plafond","ON")

@rule("RFXCOM Remote 3, button B1 & B2")
@when("Item remote_3_b_1_command_id received update")
@when("Item remote_3_b_2_command_id received update")
def rule_remote_3_b_command_id_updated(event):
    function = 'remote_control.3.b'
    log = logging.getLogger(LOG_PREFIX + '.' + function)
    log.info("Rule remote_3_b_command_id running...")
    events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_1_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_1_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_1_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_1_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_2_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_2_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_2_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_2_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_2_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_2_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_2_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_2_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_3_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_3_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_3_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_3_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_3_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_3_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_3_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_3_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_4_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_4_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_4_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_4_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_4_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_4_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_4_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_4_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")




# @item_triggered("remote_5_A", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_5_A_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# @item_triggered("remote_5_B", ITEM_UPDATE)
# def rule_remote_1_B_updated():
#     logging.info("Rule rule_remote_5_B_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","OFF")

# @item_triggered("remote_5_C", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_5_C_updated running...")
#     events.sendCommand("scene_all_off_switch","OFF")

# @item_triggered("remote_5_D", ITEM_UPDATE)
# def rule_remote_1_A_updated():
#     logging.info("Rule rule_remote_5_D_updated running...")
#     events.sendCommand("light_keuken_dimmer_plafond","ON")

# class rule_remote_3_a_test(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ChannelEventTrigger(channelUID="rfxcom:lighting4:d10d8fa9:518143") ]
#     def execute(self, module, input):
#         logging.info("Rule rule_remote_3_a_test started...")
#         logging.info(input)
# automationManager.addRule(rule_remote_3_a_test())