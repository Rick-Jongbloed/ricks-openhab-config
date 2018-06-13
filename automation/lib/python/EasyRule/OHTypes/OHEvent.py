from .. import OHImports
logger = OHImports.oh.getLogger("EasyRule.OHTypes.Event")

from OHItem import ConvertItem

class Event():
    def __init__(self, original = None):

        self.ohEvent     = original
        self.triggerType = str(original.triggerType) if original.triggerType is not None else None
        self.item        = ConvertItem(original.item)

        #type states
        # ! Item is None for Timertrigger, etc !
        self.oldState = self.item.convertValueToJython(original.oldState)   if self.item is not None else None
        self.newState = self.item.convertValueToJython(original.newState)   if self.item is not None else None
        self.command  = self.item.convertValueToJython(original.command)    if self.item is not None else None

    def __repr__(self):
        return "Event [triggerType={}, item={}, oldState={}, newState={}, command={}, ohEvent=(...)]".format(self.triggerType, self.item, self.oldState, self.newState, self.command)

