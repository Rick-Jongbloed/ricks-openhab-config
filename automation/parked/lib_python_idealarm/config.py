# -*- coding: utf-8 -*-
from org.eclipse.smarthome.core.library.types import OnOffType
from org.eclipse.smarthome.core.types import UnDefType

ON = OnOffType.ON
OFF = OnOffType.OFF
NULL = UnDefType.NULL
UNDEF = UnDefType.UNDEF

ALARM_TEST_MODE = False
LOGGING_LEVEL = 'DEBUG'
#LOGGING_LEVEL = 'INFO'
NAG_INTERVAL_MINUTES = 6

# You can define functions to determine if a sensor is enabled or not.
# These functions take 3 arguments, events itemRegistry and and log.
# The function shall return a boolean.
# def d5Enabled(events, itemRegistry, log):
#     '''
#     Door 5 sensor shall only be enabled if an Internet connection is available.
#     '''
#     return (itemRegistry.getItem('Network_Internet').state == ON)

ALARM_ZONES = [
    {
        'name': 'My Home',
        'armingModeItem': 'Z1_Arming_Mode',
        'statusItem': 'Z1_Status',
        'alertDevices': ['toggle_notification_message_pushover_alarm'],
        'sensors': [
            {'name': 'door_keuken_sensor',                              'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_voordeur_switch_status',                   'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_achterdeur_switch_status',                 'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_schuifpui_switch_status',                  'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_kantoor_raam_switch_status',               'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_slaapkamer_raam_switch_status',            'sensorClass': 'B', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_sunny_switch_status',                      'sensorClass': 'B', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_opslag_raam_switch_status',                'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_spacecave_raam_links_switch_status',       'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True},
            {'name': 'sensor_spacecave_raam_rechts_switch_status',      'sensorClass': 'A', 'nag': False,   'nagTimeoutMins': 4, 'armWarn': True,  'enabled': True}
        ],
        'armAwayToggleSwitch': 'Toggle_Z1_Armed_Away',
        'armHomeToggleSwitch': 'Toggle_Z1_Armed_Home',
        'mainZone': True,
        'canArmWithTrippedSensors': False
    }
]