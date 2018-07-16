scriptExtension.importPreset("RuleSimple")
scriptExtension.importPreset("RuleSupport")

from openhab.log import logging
from openhab.triggers import StartupTrigger, CronTrigger
from openhab import date
from openhab.actions import Pushover

import datetime
from dateutil.relativedelta import relativedelta
import json
import requests
from java.util import Calendar, GregorianCalendar

class rule_process_ical(SimpleRule):
    def __init__(self):
        self.triggers = [ 
                StartupTrigger(),
                CronTrigger("0 0 6 1/1 * ? *")              # cron: every day...
                ]

    def execute(self, module, input):
        logging.info("Rule: rule_process_ical started")

        # retrieve datetimes
        now = datetime.datetime.now()
        date_later = now + relativedelta(months=1)

        #format dates for JSON query (dates seem to be ignored, a whole year is returned)
        now_date_formatted = now.strftime("%Y-%m-%d")
        date_later_formatted = date_later.strftime("%Y-%m-%d")
        data = '{"companyCode":"53d8db94-7945-42fd-9742-9bbc71dbe4c1","startDate":"' + now_date_formatted + '","endDate":"' + date_later_formatted + '","uniqueAddressID":"ec1e04f573c98af535d861d0f3e10a3b87bdfe5e"}'

        # setup request
        host = "http://wasteapi2.2go-mobile.com/api/GetCalendar"
        headers = {"content-type":"application/json"}
        r = requests.post(host, data=data, headers=headers)

        # parse return value
        json_message = r.json()
        data_list = json_message['dataList']

        # loop through list to filter several types
        pickup_types = []
        for calendar_item in data_list:
            
            # get the next pickup event
            earliest = min([datetime.datetime.strptime(d,'%Y-%m-%dT%H:%M:%S') + relativedelta(hours=9) for d in calendar_item['pickupDates'] if datetime.datetime.strptime(d, '%Y-%m-%dT%H:%M:%S') + relativedelta(hours=9) > now])
            
            # create string for openhab item
            calendar_type = calendar_item['_pickupTypeText'].lower()    
            openhab_item_name = "afvalkalender_" + calendar_type

            # Set item
            if openhab_item_name in items:
                openhab_date = datetime.datetime.strftime(earliest,'%Y-%m-%dT%H:%M:%S')
                events.postUpdate(openhab_item_name,openhab_date)
                
                # make dict item to get the next event 
                dict_item = {earliest:openhab_item_name}
                pickup_types.append(dict(dict_item))

        # Get the next event
        earliest_overall = min(pickup_types)
        for earliest_overall_item in earliest_overall:
            
            # update item
            events.postUpdate("afvalkalender_earliest",earliest_overall[earliest_overall_item])

automationManager.addRule(rule_process_ical())

class rule_notify_afvalkalender(SimpleRule):
    def __init__(self):
        self.triggers = [ 
#                StartupTrigger(),           # for testing
                CronTrigger("0 0 19 1/1 * ? *"),              # cron: check every day @ 19:00
                CronTrigger("0 0 21 1/1 * ? *")              # cron: check every day @ 21:00 
                ]
    
    def execute(self, module, input):
        now = datetime.datetime.now()
        earliest_garbage_retrieval_type = str(items.afvalkalender_earliest)
        garbage_retrieval_datetime = getattr(items, earliest_garbage_retrieval_type)
        logging.info (garbage_retrieval_datetime)
        garbage_retrieval_datetime_python = date.to_python_datetime(garbage_retrieval_datetime)
        delta = garbage_retrieval_datetime_python - now
        if delta.days == 0: 
            if earliest_garbage_retrieval_type == "afvalkalender_packages":
                garbage_description = "plastic"
            elif earliest_garbage_retrieval_type == "afvalkalender_paper":
                garbage_description = "papier"
            elif earliest_garbage_retrieval_type == "afvalkalender_greengrey":
                garbage_description = "duo"
            msg = "Morgenochtend wordt de " + garbage_description + "bak geleegd!"
            logging.info("Posting msg: " + msg)
            Pushover.sendPushoverMessage(Pushover.pushoverBuilder(msg))

automationManager.addRule(rule_notify_afvalkalender())