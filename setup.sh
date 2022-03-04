#!/bin/bash

PWD=$(pwd)
mkdir -p $HOME/.config/systemd/user
sudo ln -s $PWD/ip_push.service $HOME/.config/systemd/user/ip_push.service
