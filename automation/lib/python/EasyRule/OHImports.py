"""
This module simulates the globals defined exported from the JSR223 bundle. It's primarily useful
if you want to work with rules and scripts in an IDE or from the command line.
"""

from org.openhab.core.jsr223.internal.shared import (
    Rule, RuleSet, ChangedEventTrigger, UpdatedEventTrigger, CommandEventTrigger,
    Event, EventTrigger, StartupTrigger, ShutdownTrigger, TimerTrigger,
    TriggerType, Openhab)

from org.openhab.core.library.types import (
    DateTimeType, StringType, PointType, StopMoveType,
    OnOffType, OpenClosedType, HSBType, IncreaseDecreaseType, DecimalType,
    PercentType, UpDownType)

from org.openhab.core.jsr223.internal.engine.scriptmanager import ScriptManager
from org.openhab.model.script.actions import BusEvent
from org.openhab.core.persistence.extensions import PersistenceExtensions
# from org.openhab.core.persistence import HistoricItem

from org.openhab.core.types import (State, Command)
from org.joda.time import DateTime

# from org.apache.commons.lang import StringUtils
# from org.apache.commons.io import (FileUtils, FilenameUtils)
# from java.net import URLEncoder
# from java.io import File
# from org.openhab.library.tel.types import CallType

oh = Openhab

if ScriptManager.getInstance():
    ItemRegistry = ir = ScriptManager.getInstance().getItemRegistry()

from org.openhab.core.types import UnDefType

session = {}