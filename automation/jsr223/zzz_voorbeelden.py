# COLOR LAMP
    # # test_item_2 = itemRegistry.getItem("light_eettafel_color").state
    # # type_test_item_2 = type(test_item_2)
    # # logging.info(type_test_item_2)
    # # logging.info(test_item_2)

    # # get lamp info
    # test_item_1 = items.light_eettafel_color
    # type_test_item_1 = type(test_item_1)
    # logging.info(type_test_item_1)
    # logging.info(test_item_1)

    # # Maybe later split HSBType into the specific parts
    
    
    # # ******** create HSBType ********
    # # var DecimalType hue = new DecimalType(240) # 0-360; 0=red, 120=green, 240=blue, 360=red(again)
    # # var PercentType sat = new PercentType(100) # 0-100
    # # var PercentType bright = new PercentType(100) # 0-100
    # # var HSBType light = new HSBType(hue,sat,bright)
    # hue = DecimalType(100.555)
    # # type_hue = type(hue)
    # # logging.info(type_hue)
    # # logging.info(hue)

    # sat = PercentType(100)
    # # type_sat = type(sat)
    # # logging.info(type_sat)
    # # logging.info(sat)

    # bright = PercentType(100)
    # # type_bright = type(bright)
    # # logging.info(type_bright)
    # # logging.info(bright)

    # light = HSBType(hue,sat,bright)
    # # type_light = type(light)
    # # logging.info(type_light)
    # # logging.info(light)

#     class rule_toggle_notification_light_eettafel(SimpleRule):
#     def __init__(self):
#         self.item_name = "toggle_notification_light_eettafel"
#         self.triggers = [ ItemCommandTrigger(self.item_name, command="ON") ]
#     def execute(self, module, input):
#         logging.info("ALARM: EETTAFEL: START")
        
#         # initialize LIFX lamp (later)
#         # get current lamp settings (store these) 
#         # turn light red 
#         # wait 5 seconds
#         # turn light off (later previous settings)

#         # get lamp info
#         #logging.info(items.light_eettafel_color)

#         # Maybe later split HSBType into the specific parts
#         hue = DecimalType(100.555)
#         sat = PercentType(100)
#         bright = PercentType(100)
#         light = HSBType(hue,sat,bright)
        
#      #   logging.info("ALARM: EETTAFEL: LICHT AAN")
#         events.sendCommand("light_eettafel_color", str(light))
#         #events.sendCommand("light_eettafel_color", str(light_test)
#     #    logging.info("ALARM: EETTAFEL: DELAY: 5 SEC START")
#         time.sleep(5)
#    #     logging.info("ALARM: EETTAFEL: DELAY: 5 SEC END")
#   #      logging.info("ALARM: EETTAFEL: LICHT UIT")
#         events.sendCommand("light_eettafel_color", "OFF")
#  #       logging.info("ALARM: EETTAFEL: TOGGLE UIT")
#         events.postUpdate("toggle_notification_light_eettafel", "OFF")
# #        logging.info("ALARM: EETTAFEL: EIND")
# automationManager.addRule(rule_toggle_notification_light_eettafel())