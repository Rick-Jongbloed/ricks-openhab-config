from core.log import logging, LOG_PREFIX
from core.rules import rule
from core.triggers import when
from core.osgi import get_service

scriptExtension.importPreset("RuleSupport")

@rule("Initialize rules on startup")
@when("Time cron 0/10 * * * * ?")
def initialize_rules_on_startup(event):
    function = 'rules.start_hardware_initialization'
    log = logging.getLogger(LOG_PREFIX + '.' + function)

    log.info("@@@@@@@@@@@@@@@@@@@@ Rule initialize_rules_on_startup started....")
    group = itemRegistry.getItem("g_rule_initialization_items")
    for item in group.getAllMembers():
        log.info("Initializing Harware initialization item: '" + str(item.name) + "' ...")
        events.sendCommand(item.name,"ON")        

    # Now disable the rule 
    ruleUID = filter(lambda rule: rule.name == "Initialize rules on startup", rules.getAll())[0].UID
    ruleEngine = get_service("org.eclipse.smarthome.automation.RuleManager")
    ruleEngine.setEnabled(ruleUID, False) # disable rule