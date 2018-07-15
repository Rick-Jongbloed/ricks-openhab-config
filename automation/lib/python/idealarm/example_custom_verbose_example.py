# -*- coding: utf-8 -*-
'''
custom_verbose_example.py

Custom ideAlarm functions library.
This file demonstrates a few possibilities, things you can implement in your own custom.py
Use it for inspiration. It won't work "out of the box" in your system.
'''

from org.eclipse.smarthome.core.types import UnDefType
from org.eclipse.smarthome.core.library.types import OnOffType, OpenClosedType
from lucid.log import logging, LOG_PREFIX
from logging import DEBUG, INFO, WARNING, ERROR
from org.joda.time import DateTime
from org.joda.time.format import DateTimeFormat
log = logging.getLogger(LOG_PREFIX + '.ideAlarm.custom')
from lucid.utils import PRIO, PUSHOVER_PRIO, PUSHOVER_DEF_DEV, kw, sendCommandCheckFirst, greeting
from lucid.actions import Pushover
from lucid.speak import tts
from lucid.sendsms import sms
from lucid.autoremote import autoremote
import random

# Get direct access to the JSR223 scope types and objects (for Jython modules imported into scripts)
from lucid.jsr223.scope import events, itemRegistry

NULL = UnDefType.NULL
UNDEF = UnDefType.UNDEF
ON = OnOffType.ON
OFF = OnOffType.OFF
OPEN = OpenClosedType.OPEN
CLOSED = OpenClosedType.CLOSED

ZONESTATUS = {'NORMAL': 0, 'ALERT': 1, 'ERROR': 2, 'TRIPPED': 3, 'ARMING': 4}
ARMINGMODE = {'DISARMED': 0, 'ARMED_HOME': 1, 'ARMED_AWAY': 2}

def sayHello():
    hour = DateTime.now().getHourOfDay()
    if not (hour > 7 and hour < 22):
        return
    greetings = [greeting(), 'Hello', 'Greetings', 'Hi']
    peopleAtHome = []
    for member in itemRegistry.getItem('G_Presence_Family').getAllMembers():
        if member.state.toString() == 'OPEN': peopleAtHome.append(member.label)
    random.shuffle(peopleAtHome)
    msg = random.choice(greetings)
    for i in range(len(peopleAtHome)):
        person = peopleAtHome[i]
        msg += ' '+person
        if i+2 == len(peopleAtHome):
            msg +=' and'
        elif i+1 == len(peopleAtHome):
            msg +='.'
        elif i+2 < len(peopleAtHome):
            msg +=','
    tts(msg)

def onArmingModeChange(zone, newArmingMode, oldArmingMode):
    '''
    This function will be called when there is a change of arming mode for a zone.
    oldArmingMode is None when initializing.
    '''
    if zone.zoneNumber == 1:
        if oldArmingMode is not None:
            Pushover.pushover('An Alarm Zone arming mode change for '+zone.name+' triggered, new value is: '+kw(ARMINGMODE, newArmingMode), PUSHOVER_DEF_DEV, PUSHOVER_PRIO['NORMAL'])

        if newArmingMode == ARMINGMODE['DISARMED']:
            sendCommandCheckFirst('Alarm_Status_Indicator_1', 'OFF')
            sendCommandCheckFirst('Wall_Plug_Bedroom_Fan', 'OFF')
            sayHello()
        elif newArmingMode == ARMINGMODE['ARMED_HOME']:
            sendCommandCheckFirst('Wall_Plug_Bedroom_Fan', 'ON')

        if newArmingMode != ARMINGMODE['DISARMED']:
            sendCommandCheckFirst('Alarm_Status_Indicator_1', 'ON')

    log.debug('Custom function: onArmingModeChange: '+zone.name.decode('utf-8')+' ---> '+kw(ARMINGMODE, newArmingMode))

def onZoneStatusChange(zone, newZoneStatus, oldZoneStatus, errorMessage=None):
    '''
    This function will be called when there is a change of zone status.
    oldZoneStatus is None when initializing.
    '''
    log.info('Custom function: onZoneStatusChange: '+zone.name.decode('utf-8')+' ---> '+kw(ZONESTATUS, newZoneStatus))

    if newZoneStatus == ZONESTATUS['ERROR']:
        errMes = 'Error when arming zone '+zone.name.decode('utf-8')+': '+errorMessage
        log.error(errMes)
        Pushover.pushover(errMes, PUSHOVER_DEF_DEV, PUSHOVER_PRIO['HIGH'])

    elif newZoneStatus == ZONESTATUS['ALERT']:
        # Get all sensors that have been tripped since 2 minutes regardless of their current state
        # considering that an intruder might have closed a tripped door already when this is running
        mins = 2 
        openSensors = zone.getOpenSensors(mins)
        sdf = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss")
        msg = ''
        for i in range(len(openSensors)):
            sensor = openSensors[i]
            msg += sensor.label
            msg += u' tripped ' + sdf.print(sensor.getLastUpdate())
            if i+2 == len(openSensors):
                msg +=' and '
            elif i+1 == len(openSensors):
                msg +='.'
            elif i+2 < len(openSensors):
                msg +=', '
        msg = u'Alarm in zone '+zone.name.decode('utf-8')+'. '+msg
        log.error(msg)

        if zone.alarmTestMode:
            log.info('ideAlarm in TESTING MODE')
            tts(msg, PRIO['EMERGENCY'])
            Pushover.pushover(msg, PUSHOVER_DEF_DEV, PUSHOVER_PRIO['NORMAL'])
        else:
            tts(msg, PRIO['EMERGENCY'])
            Pushover.pushover(msg, PUSHOVER_DEF_DEV, PUSHOVER_PRIO['EMERGENCY'])

    elif newZoneStatus == ZONESTATUS['TRIPPED']:
        if zone.zoneNumber == 1:
            alertText = u'Intrusion in '+zone.name.decode('utf-8')
            tts(alertText, PRIO['EMERGENCY'])

    elif newZoneStatus == ZONESTATUS['ARMING']:
        if zone.zoneNumber == 1:
            tts('sad cat', PRIO['HIGH'])

def onArmingWithOpenSensors(zone, armingMode):
    '''
    There might be open sensors when trying to arm. If so, this function gets called.
    (That doesn't necessarily need to be an error condition).
    However if the zone has been configured not to allow opened sensors during arming, 
    the zone status onZoneStatusChange will be called with status ERROR.
    '''
    isArming = True
    mins = 0
    openSensors = zone.getOpenSensors(mins, armingMode, isArming)

    msg = ''
    for i in range(len(openSensors)):
        sensor = openSensors[i]
        msg += sensor.label
        if i+2 == len(openSensors):
            msg +=' och '
        elif i+1 == len(openSensors):
            msg +='.'
        elif i+2 < len(openSensors):
            msg +=', '
    if msg != '':
        msg = u'Open sections in '+zone.name.decode('utf-8')+'. '+msg
        log.error(msg)
        tts(msg, PRIO['HIGH'])

def onNagTimer(zone, nagSensors):
    '''
    You should do something about the open doors!
    '''
    sdf = DateTimeFormat.forPattern("yyyy-MM-dd HH:mm:ss")
    logMsg = ''
    msg = ''
    for i in range(len(nagSensors)):
        sensor = nagSensors[i]
        msg += sensor.label
        logMsg += sensor.label
        logMsg += u' opened ' + sdf.print(sensor.getLastUpdate())
        if i+2 == len(nagSensors):
            msg +=' and '
            logMsg +=' and '
        elif i+1 == len(nagSensors):
            msg +='.'
            logMsg +='.'
        elif i+2 < len(nagSensors):
            msg +=', '
            logMsg +=', '
    msg = u'Open sections in '+zone.name.decode('utf-8')+'. '+msg
    log.info(msg)
    if zone.zoneNumber in [1, 3, 4] and itemRegistry.getItem('Z1_Block_Nag_Timer').state != ON:
        tts(msg, PRIO['HIGH'])
    elif zone.zoneNumber == 2 and itemRegistry.getItem('Z2_Block_Nag').state != ON:
        tts(msg, PRIO['MODERATE'])
