import logging
import urllib.parse

from requests import request

from homeassistant.components.notify import (BaseNotificationService)


REQUIREMENTS = ['requests']
# DOMAIN = 'join'
CONF_DEVICES = 'devices'
CONF_DEVICE_ID = 'id'
CONF_DEVICE_NAME = 'name'
CONF_DEVICE_ICON = 'icon'

ATTR_TARGET = 'device'
ATTR_ACTION = 'action'
ATTR_DATA = 'data'
ATTR_PHONENO = 'phone_number'

API = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?'


# noinspection PyUnusedLocal
def get_service(hass, config):
    # logger = logging.getLogger(__name__)
    # devices = config[DOMAIN].get(CONF_DEVICES)
    #
    # if not devices:
    #     logger.error('No device(s) defined')
    #     return
    #
    # if not isinstance(devices, list):
    #     devices = [devices]
    devices = None  # the part above is for future dev with an interface
    return JoinNotificationService(devices)


def execute(url):
    request('GET', API + url)
    return


class JoinNotificationService(BaseNotificationService):
        
    def send_message(self, message, **kwargs):
        logger = logging.getLogger(__name__)
        logger.warn(message)
        try:
            args = message.split('$')
        except ValueError:
            logger.error('Invalid target syntax: %s', message)
            return

        if not args[0]:
            logger.error('No target defined')
            return
        if not args[1]:
            logger.error('No action defined')
            return
        target = args[0]
        action = args[1]
        urls = JoinUrls(target)
        if action == 'ring':
            execute(urls.ring())
        else:
            if not args[2]:
                logger.error('No text defined')
                return
            data = args[2]
            if action == 'clipboard':
                execute(urls.set_clipboard(data))
            elif action == 'text':
                execute(urls.send_text(data))
            elif action == 'url':
                enc_data = urllib.parse.quote_plus(data)
                execute(urls.open_url(enc_data))
            elif action == 'sms':
                if not args[3]:
                    logger.error('No phone number defined')
                    return
                phone = args[3]
                execute(urls.send_sms(data, phone))
            else:
                logger.error("Unknown action %s", action)
                return

    def __init__(self, devices):
        self.devices = devices


class JoinUrls:

    def __init__(self, device_id):
        self.id = device_id

    def set_clipboard(self, text):
        return 'clipboard={1}&deviceId={0}'.format(self.id, text)

    def send_text(self, text):
        return 'text={1}&deviceId={0}'.format(self.id, text)

    def open_url(self, url):
        return 'url={1}&deviceId={0}'.format(self.id, url)

    def send_sms(self, text, number):
        return 'smsnumber={1}&smstext={2}&deviceId={0}'.format(self.id, number, text)

    def ring(self):
        return 'find=true&deviceId={0}'.format(self.id)
