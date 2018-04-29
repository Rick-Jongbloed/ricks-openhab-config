scriptExtension.importPreset("RuleSupport")
scriptExtension.importPreset("RuleSimple")

from openhab.triggers import ItemStateChangeTrigger
from openhab.log import logging

# ///* was:
# //import hnwqbgbl.concurrent.locks.ReentrantLock
# //import org.openhab.model.script.actions.*
# //import java.util.Date
# //
# //var java.util.concurrent.locks.ReentrantLock lock  = new java.util.concurrent.locks.ReentrantLock()
# //var Timer on_timer = null 
# //*/
# //
# //import java.util.concurrent.locks.ReentrantLock
# //import org.eclipse.smarthome.model.script.actions.Timer
# //
# //var ReentrantLock lock  = new ReentrantLock()
# //var Timer on_timer = null
# //
# //// during startup there are many updates to the 'myhome' group
# //// delay the initial population of gStateON to startup+20 seconds
# //
# //rule "What's ON - Startup"
# //    when 
# //        System started
# //    then
# //        // logDebug("rule-test","What's on - Startup: ONtimer set to start sRefresh to ON in 20 seconds")
# //        on_timer = createTimer(now.plusSeconds(20)) [|
# //		s_refresh_on.sendCommand(ON)
# //	]
# //end
# //
# //// the 'myhome' group gets multiple updates per each item change, 
# //// therefore a timer is set and only one refresh will happen,
# //// after 10 seconds from the first update
# //
# //rule "What's ON - All update"
# //    when 
# //        Item myhome received update 
# //    then
# //        lock.lock()
# //        try 
# //	{
# //            	if(on_timer.hasTerminated() ) 
# //		{

# //	//	        logDebug("rule-test","What's on - update: Timer has terminated, set new timer to start sRefresh in 10 seconds")
# //                	on_timer = createTimer(now.plusSeconds(10)) [| s_refresh_on.sendCommand(ON)]
# //            	}
# //        } 
# //        finally 
# //	{
# //            lock.unlock()
# //        }
# //end
# //
# //// g_state_on is a dynamic group that holds all Items in state ON.
# //// The group gets refreshed whenever the 'myhome' group gets an update, 
# //// i.e. whenever an item changes
# //
# //rule "What's on - refresh"
# //    when 
# //        Item s_refresh_on received update 
# //    then
# //	// remove rule
# //        g_state_on.members.filter( s | s.state == 0 || s.state == OFF).forEach[ item | g_state_on.removeMember(item) ]
# //	
# //	// add rule
# //	myhome.allMembers.filter
# //		(s | 
# //			(s.getClass().getName() == "org.openhab.core.library.items.SwitchItem" || s.getClass().getName() == "org.openhab.core.library.items.DimmerItem")
# //			&& s.state 	!= 0 
# //			&& s.state 	!= OFF 
# //			&& s.state 	!= NULL
# //			&& g_state_on.members.filter(x | x.name == s.name).size == 0
# //		).forEach[ item | g_state_on.addMember(item) ]
# //end

#   1.  timer die 30 seconden na system startup de rule triggert
#   2.  trigger op command naar ON van s_refresh_on // nu op change event
#   3.  whats_off group maken, alleen lichten en computers er in?
#   4.  group all off maken en die gebruiken.

class rule_whats_on_update_group (SimpleRule):
    def __init__(self):
        self.triggers = [ ItemStateChangeTrigger("s_refresh_on", state="ON", previousState="OFF") ] # later veranderen naar command? dan hoeft ie niet terug naar OFF
    def execute(self, module, input):
        logging.info(items.g_state_on)
automationManager.addRule(rule_whats_on_update_group())
