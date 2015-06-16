#!/bin/bash
#Need to set sticky bit to run file
# sudo chown root:root github-webhook.bash 
# sudo chmod 4755 github-webhook.bash

git pull origin master

if test $? -eq 0
then
systemctl restart gunicorn

fi
