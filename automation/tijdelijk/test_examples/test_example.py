from core.rules import rule
from core.triggers import StartupTrigger

@rule("My example rule")
class ExampleRule(object):
    """This doc comment will become the ESH Rule documentation value for Paper UI"""
    #def __init__(self):
    #    self.triggers = [ StartupTrigger().trigger ]
    
    def getEventTriggers(self):
        return [ StartupTrigger() ]

    def execute(self, module, inputs):
        self.log.info("rule executed")
