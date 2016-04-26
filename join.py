import logging
import urllib.parse

from requests import request

from homeassistant.components.notify import (ATTR_TARGET, ATTR_TITLE, BaseNotificationService)
import pprint

REQUIREMENTS = ['requests']
CONF_DEVICES = 'devices'
CONF_DEVICE_ID = 'id'
CONF_DEVICE_NAME = 'name'
CONF_DEVICE_ICON = 'icon'

API = 'https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?'


# noinspection PyUnusedLocal
def get_service(hass, config):
    logger = logging.getLogger(__name__)
    devices = config.get(CONF_DEVICES)

    if not devices:
        logger.error('No device(s) defined')
        return

    if not isinstance(devices, list):
        devices = [devices]
    device_dict = {}
    for device in devices:
        device_dict[device[CONF_DEVICE_NAME]] = device[CONF_DEVICE_ID]
    return JoinNotificationService(device_dict)


def execute(url):
    request('GET', API + url)
    return


class JoinNotificationService(BaseNotificationService):

    def send_message(self, message, **kwargs):
        logger = logging.getLogger(__name__)
        targets = kwargs.get(ATTR_TARGET)
        title = kwargs.get(ATTR_TITLE)
        args = message.split('/', 1)
        action = args[0]

        if not targets:
            logger.error('No target defined')
            return
        if not action:
            logger.error('No action defined')
            return
        urls = []
        for device in targets:
            urls.append(self.devices.get(device))

        urls = JoinUrls(urls[0]) # TODO allow multiple targets
        logger.warn(urls)
        if action == 'ring':
            execute(urls.ring())
        else:
            if not args[1]:
                logger.error('No text defined')
                return
            data = args[1]
            if action == 'clipboard':
                execute(urls.set_clipboard(data))
            elif action == 'text':
                execute(urls.send_text(data))
            elif action == 'notification':
                if not title:
                    logger.error('No title defined')
                    return
                execute(urls.set_notification(data,title))
            elif action == 'url':
                enc_data = urllib.parse.quote_plus(data)
                execute(urls.open_url(enc_data))
            elif action == 'sms':
                args = message.split('/', 2)
                if not args[3]:
                    logger.error('No phone number defined')
                    return
                data = args[2]
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

    def set_notification(self, data, title):
        return 'text={1}&title=dd{2}&deviceId={0}'.format(self.id, data, title)

    def send_sms(self, text, number):
        return 'smsnumber={1}&smstext={2}&deviceId={0}'.format(self.id, number, text)

    def ring(self):
        return 'find=true&deviceId={0}'.format(self.id)
