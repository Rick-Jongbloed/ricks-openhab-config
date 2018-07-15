
import EasyRule

import logging
logger = logging.getLogger( EasyRule.LOG_PREFIX + ".EasyRule.helper")

LOADED_TRIGGERS = False

def GetScriptHelper():
    global LOADED_TRIGGERS
    vars = EasyRule.openhab.jsr223.get_scope()

    helper = None
    for k in vars:
        if isinstance(vars[k], EasyRule.ScriptHelper):
            helper = vars[k]
            logger.debug("Found ScriptHelper '{}' ({})".format(k, vars[k].name_helper))
            if helper.script_vars is None:
                helper.script_vars = vars
            if helper.script_automation_manager is None:
                helper.script_automation_manager = EasyRule.openhab.jsr223.get_automation_manager()

    if helper is None:
        #insert class:
        helper = EasyRule.scripthelper.ScriptHelper("EasyRule.helper", script_vars=vars, automation_manager=EasyRule.openhab.jsr223.get_automation_manager())
        vars["__helper__"] = helper
        logger.debug("Injected ScriptHelper")


    #replace BusEvent registry with new one
    if 'BusEvent' not in vars:
        logger.debug("Replaced BusEvent")
        vars['BusEvent'] = vars['be'] = EasyRule.BusEvent

    if 'ItemRegistry' not in vars:
        logger.debug("Replaced ItemRegistry")
        vars['OH_itemRegistry'] = vars['itemRegistry']
        vars['OH_ir'] = vars['ir']
        vars['ItemRegistry'] = vars['ir'] = EasyRule.ItemRegistry

    if not LOADED_TRIGGERS:
        LOADED_TRIGGERS = True
        #helper.script_loaded_funcs.append(EasyRule.components.StartupTrigger.scriptLoaded)
        #helper.script_unloaded_funcs.append(EasyRule.components.StartupTrigger.scriptUnloaded)

        vars['scriptLoaded'] = helper.scriptLoaded
        vars['scriptUnloaded'] = helper.scriptUnloaded
    return helper