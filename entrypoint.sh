#!/bin/bash

cd /usr/src/app

target="${districts}"
if [ -n "$target" ]; then
  pipenv run python postgis2qfield.py -d $database -H $db_host -p $db_port -u $db_user -w $db_password -l $target
else
  pipenv run python postgis2qfield.py -d $database -H $db_host -p $db_port -u $db_user -w $db_password
fi
