from openhab.log import logging, LOG_PREFIX
from clickatell import Clickatell

def sms(message, subscriber='John'):
    '''
    Sends an SMS message through ClickaTell gateway.
    Example: sms("Hello")
    Example: sms("Hello", 'Carl')
    @param param1: SMS Text
    @param param2: Subscriber. A numeric phone number or a subscriber (String)
    '''
    log = logging.getLogger(LOG_PREFIX)

    ClickatellSender = '45123456789'
    ClickatellAPIUser = 'johndoe'
    ClickatellAPIPassw = 'riuyYGVTua8k'
    ClickatellAPIId = 1234567

    phoneNumbers = {
        'Anna': '467395646546',
        'Veronica': '461565136511'
    }

    phoneNumber = phoneNumbers.get(subscriber, None)
    if phoneNumber is None:
        if subscriber.isdigit():
            phoneNumber = subscriber
        else:
            log.error("Invalid subscriber")
            return
    gateway = Clickatell(ClickatellAPIUser, ClickatellAPIPassw, ClickatellAPIId, ClickatellSender)
    message = {'to': phoneNumber, 'text': message}
    log.info("Sending SMS to: " + str(phoneNumber))
    retval, msg = gateway.sendmsg(message)
    if retval == True:
        log.info("SMS Sent: " + msg)
    else:
        log.error("Error while sending SMS: " + str(retval))
    return
