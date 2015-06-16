#!/bin/bash

git pull origin master

if test $? -eq 0
then
systemctl restart gunicorn

fi
