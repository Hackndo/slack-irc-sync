# Slack-IRC Synchronization

Description
-----------

**Python3.5+** implementation of a synchronization between IRC and Slack

![slackirc](https://user-images.githubusercontent.com/11051803/32947338-ad9a7fe2-cb9b-11e7-8d9f-54c6a2dd7779.gif)

Requirements
------------

* Python 3.5+
* Slack bot 

Slack Bot
-----------

Go to [Create new Bot User](https://my.slack.com/services/new/bot)

Initialization
--------------

```sh
git clone git@github.com:Hackndo/slack-irc-sync.git
cd slack-irc-sync
mkvirtualenv slackirc -p $(which python3)
pip install -r requirements.txt
```

Configuration
-------------

Copy configuration template

```sh
cp config/config.json.dist config/config.json
```

Configuration file looks like this

```javascript
{
    "irc": {
        "server": "irc.server.com",                 // IRC Server
        "port": "6667",                             // IRC Port
        "ssl": false,                               // Use SSL
        "channel": "#channel",                      // IRC Channel
        "nickname": "h_bot",                        // Bot Nickname
        "owner": "username",                        // Bot Owner Nickname (admin commands)
        "log_events": true                          // Send part/join/kick/quit to slack
    },
    "slack": {
        "channel": "<channel id>",                  // Slack Channel ID
        "bot_id": "<bot ID>",                       // Slack Bot user ID
        "bot_name": "irc-sync",                     // Slack Bot Nickname
        "token": "<bot token>",                     // Slack Bot Token
        "owner": "username",                        // Slack Bot Owner username (admin commands)
        "cmd_prefix": "!",                          // Channel commands prefix (if any)
        "output_msg": "<:username:> :message:",     // Message format when Slack message is received
        "output_cmd": "CMD by :username:",          // Message format when Slack command is received
        "log_events": true                          // Send part/join/kick/quit to IRC
    },
    "formatting": {
        "irc_to_slack": false,                      // Keep bold|underline|italic from IRC to Slack
        "slack_to_irc": true                        // Keep bold|underline|italic from Slack to IRC
    }
}
```

Usage
-----

```
(slackirc) pixis@kali:~/Tools/slack-irc-sync $ python slack-irc-sync.py 
[IRC] Logged in as:
[IRC] hacknbot
[Slack] Logged in as:
[Slack] irc-sync
[Slack] <pixis> : Can you hear me IRC Tom? 😃
[IRC] <pixis> : Yes, I can
```


TODO
----

- [X] Format message from Slack to IRC
- [X] Format message from IRC to Slack : Difficult because not everything is possible, especially when formatting is overlapping
- [ ] Multi channel
- [ ] Multi server
- [ ] Dynamically relaod conf when changed
- [ ] Change conf with IRC or Slack commands
