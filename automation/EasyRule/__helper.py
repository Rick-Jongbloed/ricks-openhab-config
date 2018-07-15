import sys
import ScriptHelper
from OHTypes import ItemRegistry, BusEvent


from OHImports import oh
logger = oh.getLogger("EasyRule.helper")

def GetScriptGlobals():
  """
  Walks the Python stack and finds the script-level globals dictionary.
  """
  depth = 1
  while True:
    frame = sys._getframe(depth)
    name = str(type(frame.f_globals))
    #print(name)
    #print( "   {}".format(frame.f_globals))
    if name == "<type 'scope'>":
        return frame.f_globals
    depth += 1

def GetScriptHelper():
    vars = GetScriptGlobals()

    helper = None
    for k in vars:
        if type(vars[k]) is ScriptHelper.ScriptHelper:
            helper = vars[k]
            logger.debug("Found ScriptHelper '{}'".format(helper.logname))

    if helper is None:
        #insert class:
        helper = ScriptHelper.ScriptHelper("EasyRule.helper")
        vars["__helper__"] = helper
        logger.debug("Injected ScriptHelper")

    #insert getRules - function if necessary
    if not 'getRules' in vars:
        logger.debug("Injected getRules function")
        vars['getRules'] = helper.GetRules


    #replace item registry with new one
    if str(type(vars['ir'])) == "<type 'org.openhab.core.internal.items.ItemRegistryImpl'>":
        logger.debug("Replaced ItemRegistry")
        vars['ItemRegistry'] = vars['ir'] = ItemRegistry()


    #replace item registry with new one
    if not isinstance(vars['BusEvent'], BusEvent):
        logger.debug("Replaced BusEvent")
        vars['BusEvent'] = vars['be'] = BusEvent()


    return helper
