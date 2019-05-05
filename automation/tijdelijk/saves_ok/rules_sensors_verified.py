from core.log import logging
from core.triggers import when
from core.rules import rule
#@item_triggered("temp_badkamer_sensor_raw", event_types=ITEM_UPDATE, result_item_name="temp_badkamer_sensor_cali")
@rule("Rule for badkamer humidity updates")
@when("Item temp_badkamer_sensor_raw received update")
def rule_calibrate_temp_humid_sensor_bathroom():
    logging.info("Rule rule_calibrate_temp_humid_sensor_bathroom running...: " + str(items.temp_badkamer_sensor_raw))
    if str(items.temp_badkamer_sensor_raw) != "NULL":
        raw_temp_from_sensor = float(str(items.temp_badkamer_sensor_raw))
        temp_adjustment = float("40")
        temp_calibrated = raw_temp_from_sensor - temp_adjustment
        events.postUpdate("temp_badkamer_sensor_cali", temp_calibrated)

# #@item_triggered("router_temperature", ITEM_CHANGE)
# @when ("Item router_temperature changed")
# def rule_router_temps_split():
#     #logging.info("Rule rule_router_temps_split running...")
#     array = str(items.router_temperature).split(" ")
#     events.postUpdate("router_temperature_50_1",        array[0])
#     events.postUpdate("router_temperature_24", 	        array[1])
#     events.postUpdate("router_temperature_50_2",	array[2])
#     events.postUpdate("router_temperature_cpu", 	array[3])

