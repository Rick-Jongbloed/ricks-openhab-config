import traceback


from OHImports import Rule, oh
logger = oh.getLogger("EasyRule.Rule")



import __helper as helperfunctions

from OHTypes import Event



def SetExceptionHandler(exceptionhandler):
    if exceptionhandler.__code__.co_argcount != 2:
        logger.error("Exception Handler does not have 2 args!")
        return None

    BaseRule.ExceptionHandler = exceptionhandler



def BaseRuleDecorator( cls):

    def init(self, *args, **kwargs):
        BaseRule.__init__(self, *args, **kwargs)
        cls.__init__( self, *args, **kwargs)

    def execute(self, event):
        try:
            return cls.execute(self, Event(event) if self.ProcessEvents else event)
        except Exception as e:
            #show error
            if self.logger is not None:
                self.logger.error("{}\n{}".format( e, traceback.format_exc()))
            else:
                print("Error in '{}' : {}\n{}".format(self.name, e, traceback.format_exc()))

            #custom error handler
            if BaseRule.ExceptionHandler is not None:
                #has to be a function with 2 params
                #first is the rule, second the exception
                BaseRule.ExceptionHandler(self, e)
            return None

    #replace init with newly defined one
    derived_class = type(cls.__name__, (cls, BaseRule), {'__init__': init, 'execute' : execute})

    #what does this do?
    def new(cls, *args, **kwargs):
        return super(cls, cls).__new__(cls, *args, **kwargs)
    derived_class.__new__ = staticmethod(new)
    return derived_class


class BaseRule(Rule):

    ProcessEvents    = True
    ExceptionHandler = None

    def __init__(self, *args, **kwargs):
        super(Rule, self).__init__()

        self.logger = None
        self.name = kwargs.get("name", self.__class__.__name__)
        self.ProcessEvents = kwargs.get("ProcessEvents", BaseRule.ProcessEvents)

        if kwargs.get("AddToHelper", True):
            helper = helperfunctions.GetScriptHelper()
            helper.AddRule(self)

    #required functions
    def Initialize(self):
        pass
    def getEventTrigger(self):
        return []

    def __repr__(self):
        return "<Rule {}>".format(self.name)