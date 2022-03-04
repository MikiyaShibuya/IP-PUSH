#!/usr/bin/env python3

import os
import sys
from datetime import datetime
import subprocess
import requests
import time

root_dir = os.environ['HOME'] + '/IP-PUSH'

def get_ipaddress_text(adapter):
    res = subprocess.check_output("/usr/sbin/ifconfig " + adapter + " | awk '{ print $2}' | "
                                  "grep -E -o '([0-9]{1,3}[\.]){3}[0-9]{1,3}' | "
                                  "tr -d '\n'", shell=True).decode('utf-8')
    return res

def push_message(uri, message):
    payload = '{"text":"' + message + '"}'
    return requests.post(uri, data=payload)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Error: A txt file that contains slack uri must be given as an argument')
        exit(1)

    with open(sys.argv[1]) as f:
        uri = f.readline()

    prev_ip = '0.0.0.0'

    while(True):

        ip_addr = get_ipaddress_text('eth0')

        if ip_addr != prev_ip:
            prev_ip = ip_addr

            # Push message to slack
            text = f'NAS-PI\n - Local IP: {ip_addr}'
            response = push_message(uri, text)

            # Record log
            log_fn = root_dir + '/ip_push.log'
            time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_fn, 'a') as f:
                f.write(time_str + '\n' + str(response) + '\n')


        time.sleep(60 * 5)

