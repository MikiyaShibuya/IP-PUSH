#!/usr/bin/env python3

import os
from slack_sdk.web import WebClient
import subprocess


def get_ipaddress_text(adapter):
    res = subprocess.check_output("ifconfig " + adapter + " | awk '{ print $2}' | "
                                  "grep -E -o '([0-9]{1,3}[\.]){3}[0-9]{1,3}' | "
                                  "tr -d '\n'", shell=True).decode('utf-8')
    return res



if __name__ == "__main__":
    token = 'xoxb-729259314595-2423215791607-K4iHO1QloyB88jOEWg03tCC1'
    client = WebClient(token)

    channel = '#webhook'
    text = get_ipaddress_text('eth0')

    print(text)

    response = client.chat_postMessage(text=text, channel=channel)
