from openhab.log import logging
from openhab.triggers import item_triggered, ITEM_UPDATE, ITEM_CHANGE

@item_triggered("temp_badkamer_sensor_raw", event_types=ITEM_UPDATE, result_item_name="temp_badkamer_sensor_cali")
def rule_calibrate_temp_humid_sensor_bathroom():
    #logging.info("Rule rule_calibrate_temp_humid_sensor_bathroom running...")
    if str(items.temp_badkamer_sensor_raw) != "NULL":
        raw_temp_from_sensor = float(str(items.temp_badkamer_sensor_raw))
        temp_adjustment = float("40")
        temp_calibrated = raw_temp_from_sensor - temp_adjustment
        return temp_calibrated

@item_triggered("router_temperature", ITEM_CHANGE)
def rule_router_temps_split():
    #logging.info("Rule rule_router_temps_split running...")
    array = str(items.router_temperature).split(" ")
    events.postUpdate("router_temperature_50_1",    array[0])
    events.postUpdate("router_temperature_24", 	    array[1])
    events.postUpdate("router_temperature_50_2",	array[2])
    events.postUpdate("router_temperature_cpu", 	array[3])

