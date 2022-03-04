# IP-PUSH
Watch ip address and notfy as a slack bot after reboot or when address was changed.

## Installation
```
git clone git@github.com:MikiyaShibuya/IP-PUSH.git
cd IP-PUSH
./setup.sh
echo <slack webhook URI> >> slack_uri.txt
echo <display name for slack message> >> slack_uri.txt
systemctl --user enable ip_push.service
systemctl --user start ip_push.service
```
