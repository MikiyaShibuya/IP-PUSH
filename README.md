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
## How to generate slack incoming webhook URL
link: https://api.slack.com/apps
1. Create app
2. Select your slack channel according to instruction to complete creation
3. Activate "Incoming webhooks", from left tab
4. Click "Add new webhook to workspace", then choose channel where ip-address will be sent to
5. The url will appear in list
