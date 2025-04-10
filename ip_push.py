#!/usr/bin/env python3

import os
import sys
import re
from datetime import datetime
import subprocess
import requests
import time
from typing import List

root_dir = os.path.dirname(__file__)

def get_ipaddress_text(adapter):
    res = subprocess.check_output("/usr/sbin/ifconfig " + adapter + " | awk '{ print $2}' | "
                                  "grep -E -o '([0-9]{1,3}[\.]){3}[0-9]{1,3}' | "
                                  "tr -d '\n'", shell=True).decode('utf-8')
    return res

# Split input string and filter ip address
# Subnet mask, default gateway, etc will be rejected
def find_address(text: str) -> List[str]:
    cands = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",text)

    ips = []
    for cand in cands:
        try:
            last_num = int(cand.split('.')[-1])
            if last_num not in [0, 1, 255]:
                ips.append(cand)
        except Exception as e:
            print(e)

    return ips


def get_ipaddress_list() -> str:
    res = subprocess.check_output("/usr/sbin/ifconfig", shell=True).decode('utf-8')
    lines = res.split('\n')
    ips = []
    [ips.extend(find_address(line)) for line in lines]

    ips.sort()

    return ' / '.join(ips)

def push_message(uri, message):
    payload = '{"text":"' + message + '"}'
    return requests.post(uri, data=payload)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Error: A txt file that contains slack uri must be given as an argument')
        print(f'Note: Current IP Address: {get_ipaddress_list()}')
        exit(1)

    with open(sys.argv[1]) as f:
        uri = f.readline().split('\n')[0]
        device_name = f.readline().split('\n')[0]

    prev_ip = '0.0.0.0'

    while(True):

        ip_addr = get_ipaddress_list()

        if ip_addr != prev_ip:
            prev_ip = ip_addr

            # Push message to slack
            text = f'{device_name}\n - Local IP: {ip_addr}'
            response = push_message(uri, text)

            # Record log
            log_fn = root_dir + '/ip_push.log'
            time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_fn, 'a') as f:
                f.write(f'{time_str} {text} {response.status_code}\n')


        time.sleep(60 * 5)

