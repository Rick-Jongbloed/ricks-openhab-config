
# from core.rules import rule
# from core.triggers import when, CronTrigger


# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")
# class RawAPICron(SimpleRule):
#     def __init__(self):
#         self.triggers = [
#             TriggerBuilder.create()
#                     .withId("Hello_World_Cron_Trigger")
#                     .withTypeUID("timer.GenericCronTrigger")
#                     .withConfiguration(
#                         Configuration({
#                             "cronExpression": "0/10 * * * * ?"
#                         })).build()
#         ]
#         self.name = "Hello world cron rule (raw API)"
#         self.description = "This is an example cron rule using the raw API"
# #        self.tags = [ "Test tag" ]
#     def execute(self, module, inputs):
#         self.log.info("This is a 'hello world!' from a Jython rule (raw API): Cron")
# automationManager.addRule(RawAPICron())

# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")
# # make sure you have an item named Test_Switch_1, or swap out the item for one that already exists
# class RawAPIStateUpdate(SimpleRule):
#     def __init__(self):
#         self.triggers = [
#             TriggerBuilder.create()
#                 .withId("Hello_World_State_Update_Trigger")
#                 .withTypeUID("core.ItemStateUpdateTrigger")
#                 .withConfiguration(
#                     Configuration({
#                         "itemName": "Test_Switch_1"
#                     }))
#                 .build()
#         ]
#         self.name = "Hello world item state update rule (raw API)"
#     def execute(self, module, input):
#         self.log.info("This is a 'hello world!' from a Jython rule (raw API): ItemStateUpdateTrigger")
# automationManager.addRule(RawAPIStateUpdate())


# DOESN"T WORK
# from core.triggers import CronTrigger
# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")
# # requires CronTrigger import
# class ExtensionCron(SimpleRule):
#     def __init__(self):
#         self.triggers = [ CronTrigger("0/10 * * * * ?").trigger ]
#         self.name = "Hello world cron rule (extension)"
    
#     def execute(self, module, inputs):
#         self.log.info("This is a 'hello world!' from a Jython rule (extension): CronTrigger")
# automationManager.addRule(ExtensionCron())


## DOESN"T WORK - self.log.info doesn't seem to work! (TODO)
## self.log.info does work!
# scriptExtension.importPreset("RuleSupport")
# scriptExtension.importPreset("RuleSimple")
# from core.triggers import ItemStateUpdateTrigger
# from core.log import logging      # CUSTOM
# class ExtensionItemUpdate(SimpleRule):
#     def __init__(self):
#         self.triggers = [ ItemStateUpdateTrigger("Test_Switch_1").trigger ]
#         self.name = "Hello world item state update rule (extension)"
    
#     def execute(self, module, inputs):
#         logging.info("1 This is a 'hello world!' from a Jython rule (extension): ItemStateUpdateTrigger") # Works, not default
#         self.log.info("2")                                                                                  # does not work
#         self.log.info("2 This is a 'hello world!' from a Jython rule (extension): ItemStateUpdateTrigger")  # does not work
# automationManager.addRule(ExtensionItemUpdate())    # works


## WORKS
# from core.triggers import CronTrigger
# from core.rules import rule
# @rule("Hello world cron rule (extension with rule decorator)")
# class ExtensionCronWithRule(object):
#     def __init__(self):
#         self.triggers = [ CronTrigger("0/10 * * * * ?").trigger ]
#         self.name = "Hello world cron rule (extension with rule decorator)"
    
#     def execute(self, module, inputs):
#         self.log.info("This is a 'hello world!' from a Jython rule (extension): CronTrigger")

## WORKS
# from core.triggers import ItemStateUpdateTrigger
# from core.rules import rule
# @rule("Hello world item update rule (extension with rule decorator)")
# class ExtensionItemUpdateWithRule(object):
#     def __init__(self):
#         self.triggers = [ ItemStateUpdateTrigger("Test_Switch_1").trigger ]
#         self.name = "Hello world item update rule (extension with rule decorator)"
    
#     def execute(self, module, inputs):
#         self.log.info("This is a 'hello world!' from a Jython rule (extension with rule): ItemUpdateTrigger")


## WORKS
# from core.rules import rule
# from core.triggers import when

# @rule("Hello World cron rule (decorator)", description="This is an example rule that demonstrates using a cron rule with decorators", tags=["Test tag", "Hello World"])# [description and tags are optional]
# @when("Time cron 0/10 * * * * ?")
# def hellowWorldDecoratorCron(event):
#     hellowWorldDecoratorCron.log.info("This is a 'hello world!' from a Jython rule (decorator): Cron")

## WORKS
# from core.rules import rule
# from core.triggers import when
# @rule("Hello World item update rule (decorator)")
# @when("Item Test_Switch_1 received update")
# def hellowWorldDecoratorItemUpdate(event):
#     hellowWorldDecoratorItemUpdate.log.info("This is a 'hello world!' from a Jython rule (decorator): Item update")

