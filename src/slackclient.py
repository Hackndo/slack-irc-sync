#!/usr/bin/env python3

import asyncio
import threading
import time
import os
from slackclient import SlackClient
from .formatting import S2IFormatter


class SlackClient(SlackClient):
    def __init__(self, configuration):
        self.h_token = configuration['slack']['token']
        self.h_channel = configuration['slack']['channel']
        self.h_bot_id = configuration['slack']['bot_id']
        self.h_bot_name = configuration['slack']['bot_name']
        self.h_owner = configuration['slack']["owner"]
        self.h_cmd_prefix = configuration['slack']["cmd_prefix"]
        self.h_output_msg = configuration['slack']["output_msg"]
        self.h_output_cmd = configuration['slack']["output_cmd"]
        self.h_log_events = configuration['slack']["log_events"]
        self.h_formatter = S2IFormatter(configuration)
        self.h_irc = None

        super().__init__(self.h_token)

    def parse_slack_output(self, slack_rtm_output):
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output:
                    self.dispatch_message(output)


    def dispatch_message(self, output):
        if "user" not in output or output['user'] == self.h_bot_id:
            return

        user = self.get_nick(output['user'])
        
        if output["type"] == "message":
            """
            on message
            """
            print("[Slack] <%s> %s" % (user, output['text']))
            self.h_send_to_irc(user, self.h_format_text(output['text']))

        elif self.h_log_events:
            if output["type"] == "presence_change":
                """
                on status change
                """
                if output["presence"] == "away":
                    message = "%s has quit" % user
                elif output['presence'] == "active":
                    message = "%s has joined" % user
                self.h_raw_send_to_irc(message)

            elif output["type"] == "member_joined_channel":
                message = "%s has joined" % user
                self.h_raw_send_to_irc(message)

    def set_irc(self, irc):
        self.h_irc = irc

    def on_message(self, message):
        pass

    def get_nick(self, user_id):
        user = self.api_call('users.info', user=user_id)
        if user['ok']:
            if user['user']['profile']['display_name'] != '':
                return user['user']['profile']['display_name']
            return user['user']['profile']['real_name']
        return None

    def h_raw_send_to_irc(self, message):
        print("[Slack] %s" % message)
        self.h_irc.h_send_message(message)

    def h_send_to_irc(self, username, content):
        message = self.h_output_msg.replace(":username:", username).replace(":message:", content)

        if content.startswith(self.h_cmd_prefix):
            self.h_irc.h_send_message(self.h_output_cmd.replace(":username:", username))
            self.h_irc.h_send_message(content)
        else:
            self.h_irc.h_send_message(message)

    def h_send_message(self, user, message):
        self.api_call("chat.postMessage", channel=self.h_channel,
                          text=message, as_user=False, username=user)

    def h_format_text(self, message):
        return self.h_formatter.format(message)

    def h_run(self):
        READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
        if self.rtm_connect():
            print("[Slack] Logged in as:")
            print("[Slack] %s" % self.h_bot_name)
            while True:
                self.parse_slack_output(self.rtm_read())
                time.sleep(READ_WEBSOCKET_DELAY)
        else:
            print("Connection failed. Invalid Slack token or bot ID?")
