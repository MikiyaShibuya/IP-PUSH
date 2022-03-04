#!/usr/bin/env python3

import os
from datetime import datetime
from slack_sdk.web import WebClient
import subprocess


def get_ipaddress_text(adapter):
    res = subprocess.check_output("/usr/sbin/ifconfig " + adapter + " | awk '{ print $2}' | "
                                  "grep -E -o '([0-9]{1,3}[\.]){3}[0-9]{1,3}' | "
                                  "tr -d '\n'", shell=True).decode('utf-8')
    return res


if __name__ == "__main__":

    token = 'xoxb-729259314595-2423215791607-K4iHO1QloyB88jOEWg03tCC1'
    client = WebClient(token)

    channel = '#ip-push'
    ip_addr = get_ipaddress_text('eth0')

    text = f'NAS-PI\n - IP address: {ip_addr}'

    response = client.chat_postMessage(text=text, channel=channel)

    log_fn = os.environ['HOME'] + '/ip_push.log'
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_fn, 'a') as f:
        f.write(time_str + '\n' + str(response) + '\n')

