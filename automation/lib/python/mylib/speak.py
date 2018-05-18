import os
from mylib.utils import PRIO, getItemValue

from openhab.log import logging, LOG_PREFIX
from org.joda.time import DateTime

def tts(ttsSay, ttsPrio=PRIO['MODERATE'], **keywords):
    '''
    Text To Speak function. First argument is positional and mandatory.
    Remaining arguments are optionally keyword arguments.
    Example: tts("Hello")
    Example: tts("Hello", PRIO['HIGH'], ttsRoom='Kitchen', ttsVol=42, ttsLang='en-GB', ttsVoice='Brian')
    @param param1: Text to speak (positional argument)
    @param param2: Priority as defined by PRIO. Defaults to PRIO['MODERATE']
    @param ttsRoom: Room to speak in. Defaults to "All".
    @return: this is a description of what is returned
    '''
    module_name = 'speak'
    log = logging.getLogger(LOG_PREFIX+'.'+module_name+'.tts')
    ttsRoom = 'All' if 'ttsRoom' not in keywords else keywords['ttsRoom']
    ttsVol = None if 'ttsVol' not in keywords else keywords['ttsVol']
    ttsLang = 'sv-SE' if 'ttsLang' not in keywords else keywords['ttsLang']
    ttsVoice = 'Astrid' if 'ttsVoice' not in keywords else keywords['ttsVoice']

    if not ttsVol or ttsVol >= 70:
        if ttsPrio == PRIO['LOW']:
            ttsVol = 30
        elif ttsPrio == PRIO['MODERATE']:
            ttsVol = 40
        elif ttsPrio == PRIO['HIGH']:
            ttsVol = 60
        elif ttsPrio == PRIO['EMERGENCY']:
            ttsVol = 70
        else:
            ttsVol = 50

    hour = DateTime.now().getHourOfDay()
    # (ideAlarm.isArmed('Bostaden') and ttsPrio <= PRIO['MODERATE']): didn't work out due to circulare reference of ideAlarm
    if (hour < 7 or hour > 21) or \
        ((getItemValue('Z1_Arming_Mode', 0) != 0) and ttsPrio <= PRIO['MODERATE']):
        log.info("TTS: ttsPrio is to low to speak \'" + ttsSay + "\' at this moment")
        return False

    log.info("TTS: Speaking \'" + ttsSay + "\'")
    # The following will execute as user openhab and that users public key
    # **must** have been added into authorized_keys
    os.system('/home/john/node-sonos2domo/speak.sh ' \
        + ttsRoom + ' ' + str(ttsVol) + ' ' + ttsLang + ' ' + ttsVoice + ' ' + ttsSay \
        + ' > /dev/null 2>&1 &')
    return True
