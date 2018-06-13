
from java.nio.file.StandardWatchEventKinds import ENTRY_CREATE, ENTRY_DELETE, ENTRY_MODIFY

import json
import uuid

from org.eclipse.smarthome.automation           import Trigger          as _Trigger
from org.eclipse.smarthome.automation           import Module           as _Module
from org.eclipse.smarthome.automation.handler   import TriggerHandler   as _TriggerHandler
from org.eclipse.smarthome.automation.type      import TriggerType      as _TriggerType
from org.eclipse.smarthome.config.core          import Configuration    as _Configuration


import openhab
from EasyRule.openhab.jsr223 import scope, get_automation_manager
scope.scriptExtension.importPreset("RuleSimple")

from EasyRule.openhab.osgi.events import OsgiEventTrigger

# --------------------------------------------------------------------------------

class BaseTrigger(_Trigger):
    def __init__(self, _type, _config, name=None):
        _Trigger.__init__(self, uuid.uuid1().hex if name is None else name, _type, _config)

    def SetTriggerID(self, name):
        id_field = type(_Module).getClass(_Module).getDeclaredField(_Module, "id")
        id_field.setAccessible(True)
        id_field.set(self, name)

# Item Triggers
class ItemReceivedUpdate(BaseTrigger):
    def __init__(self, itemName, state=None, **kwargs):
        self.config = { "itemName": itemName }
        if state is not None:
            self.config["state"] = state
        BaseTrigger.__init__(self, "core.ItemStateUpdateTrigger", _Configuration(self.config), **kwargs) 

class ItemChanged(BaseTrigger):
    def __init__(self, itemName, state=None, **kwargs):
        self.config = { "itemName": itemName }
        if state is not None:
            self.config["state"] = state
        BaseTrigger.__init__(self, "core.ItemStateChangeTrigger", _Configuration(self.config), **kwargs) 

class ItemReceivedCommand(BaseTrigger):
    def __init__(self, itemName, command=None, **kwargs):
        self.config = { "itemName": itemName }
        if command is not None:
            self.config["command"] = command
        BaseTrigger.__init__(self, "core.ItemCommandTrigger", _Configuration(self.config), **kwargs) 



# --------------------------------------------------------------------------------
# Cron Trigger
EVERY_SECOND = "0/1 * * * * ?"
EVERY_MINUTE = "0 * * * * ?"
EVERY_HOUR = "0 0 * * * ?"

class CronTrigger(BaseTrigger):
    def __init__(self, cronExpression, **kwargs):
        BaseTrigger.__init__(self, "timer.GenericCronTrigger", _Configuration({
                "cronExpression": cronExpression
                }), **kwargs) 

class StartupTrigger(BaseTrigger):
    def __init__(self, **kwargs):
        BaseTrigger.__init__(self, openhab.STARTUP_MODULE_ID, _Configuration(), **kwargs) 


class ItemEventTrigger(BaseTrigger):
    def __init__(self, eventSource, eventTypes, eventTopic="smarthome/items/*", **kwargs):
        self.triggerName = self.triggerName
        BaseTrigger.__init__(self, "core.GenericEventTrigger", _Configuration({
                "eventTopic": eventTopic,
                "eventSource": "smarthome/items/{:s}/".format(eventSource),
                "eventTypes": eventTypes
                }), **kwargs) 




# --------------------------------------------------------------------------------
# ItemRegistryTriggers
class _ItemRegistryTrigger(OsgiEventTrigger):
    def __init__(self, event_name):
        OsgiEventTrigger.__init__(self)
        self.event_name = event_name
        
    def event_filter(self, event):
        return event.get('type') == self.event_name
    
    def event_transformer(self, event):
        return json.loads(event['payload'])

class ItemRegistryItemAdded(_ItemRegistryTrigger):
    def __init__(self):
        _ItemRegistryTrigger.__init__(self, "ItemAddedEvent")
        
class ItemRegistryItemRemoved(_ItemRegistryTrigger):
     def __init__(self):
         _ItemRegistryTrigger.__init__(self, "ItemRemovedEvent")

class ItemRegistryItemUpdated(_ItemRegistryTrigger):
    def __init__(self):
        _ItemRegistryTrigger.__init__(self, "ItemUpdatedEvent")



# Directory watcher _Trigger
class DirectoryEvent(BaseTrigger):
    def __init__(self, path, event_kinds=[ENTRY_CREATE, ENTRY_DELETE, ENTRY_MODIFY], watch_subdirectories=False):
        triggerId = type(self).__name__ + "-" + uuid.uuid1().hex
        self.config = {
            'path': path,
            'event_kinds': str(event_kinds),
            'watch_subdirectories': watch_subdirectories,
        }
        BaseTrigger.__init__(self, triggerId, openhab.DIRECTORY_TRIGGER_MODULE_ID, _Configuration(self.config))




