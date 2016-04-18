## A Join notifier for Home Assistant

[Join](http://joaoapps.com/join) is similar to Pushbullet, it allows you to push information to different devices.
It's a paid app with a trial period.

[Home Assistant](https://home-assistant.io/) is an open-source home automation platform running on Python 3.

Installation:

- put `join.py` into `<home-assistant-config>/custom_components/notify/`
(`<home-assistant-config>` is usually in `/username/.homeassistant` on Linux)
- add a notifier to your `configuration.yaml` file

```yaml
notify:
  - name: join
    platform: join
```

- You can now use the Join notifier like any other notifier:

```yaml
automation:
    - alias: Test ring
      trigger:
        platform: state
        entity_id: input_boolean.activate_join
        to: 'on'
      action:
        service: notify.join
        data:
          message: '<join-device-id>$<action>$<data>$<phone-number>'
```

Message configuration is split by `$`-signs (If you want to use one in your message you are out of luck for now):

- **\<join-device-id>** (*Required*): Get yours from [the Join http api site](https://joinjoaomgcd.appspot.com/)
- **\<action>** (*Required*): One of
    - ring: rings the device on full volume
    - text: sends a text command, useful for apps like Tasker
    - sms: sends an sms
    - url: opens an url on the device
    - clipboard: set the clipboard on the device
- **\<data>** (*Optional* for 'ring', *Required* for all others): The data (text, url) for the command
- **\<phone-number>** (*Optional* for all but 'sms'): The number to send the SMS to

**Disclaimer:** The code could probably be much, much better.
But I don't really know Python and I haven't yet done much with Home Assistant.

This project is not an official Join by joaoapps product I do not own
any copyright or trademarks regarding Join.
