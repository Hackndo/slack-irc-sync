#!/usr/bin/env python3

import json
import os

from src.ircclient import IRCClient
from src.slackclient import SlackClient

with open(os.path.join("config", "config.json"), encoding="utf-8") as f:
    settings = json.loads(f.read())

slack_client = SlackClient(settings)
irc_client = IRCClient(settings)

slack_client.set_irc(irc_client)
irc_client.set_slack(slack_client)


irc_client.h_run()
slack_client.h_run()
