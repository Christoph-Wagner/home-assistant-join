## A Join notifier for Home Assistant

[Join](http://joaoapps.com/join) is similar to Pushbullet, it allows you to push information to different devices.
It's a paid app with a trial period.

[Home Assistant](https://home-assistant.io/) is an open-source home automation platform running on Python 3.

Installation:

- put `join.py` into `<home-assistant-config>/custom_components/notify/`
(`<home-assistant-config>` is usually in `/username/.homeassistant` on Linux)
- add the notifier to your `configuration.yaml` file

```yaml
notify:
  - name: join
    platform: join
    devices:
    - id: '<join-device-id>'
      name: 'Phone'
    - id: '<join-device-id>'
      name: 'Other Phone'
    - id: '<join-device-id>'
      name: 'Browser'
```
Get the \<join-device-id> from [the Join http api site](https://joinjoaomgcd.appspot.com/)
- You can now use the Join notifier like any other notifier:

```yaml
automation:
    - alias: Test Join
      trigger:
        platform: state
        entity_id: input_boolean.activate_join
        to: 'on'
      action:
        service: notify.join
      data:
        target:
          - 'Phone'
          - 'Browser'
        title: <title>
        message: '<action>/[<phone-number>/]<data>'
```

- **\<action>** (*Required*): One of
    - ring: rings the device on full volume
    - text: sends a text command, useful for apps like Tasker
    - sms: sends an sms
    - url: opens an url on the device
    - clipboard: set the clipboard on the device
    - notification: sends an notification
- **\<data>** (*Optional* for 'ring', *Required* for all others):
The data (text, url) for the command
- **\<title>** (*Optional*) Set the notification title if action == notification
- **\<phone-number>** (*Optional* for all but 'sms'): The number to send the SMS to
- **target** (*Required*) A list of device names, currently only the first is working

**Changelog**:
- 2016-04-26: **0.1.0**
    - Friendly names for devices
    - Added notification capabilities
- 2016-04-18: Initial release **0.0.1**

**Roadmap**
- Add Icon capabilities (for notifications)
- Allow events to be sent to multiple devices
- Add homeassistant 'mdi:icon' format support for icons
- Add to home-assistant as official component

**Disclaimer:** The code could probably be much, much better.
But I don't really know Python and I haven't yet done much with Home Assistant.

This project is not an official Join by joaoapps product I do not own
any copyright or trademarks regarding Join.
