#!/usr/bin/env bash
set -uex
set -o pipefail


if [ "$#" -ne 1 ]
then
  echo "FATAL: Please supply a single dashboard ID to operate on, exiting"
  exit 1
fi

# Check our variables are correctly configured
echo "CRUDDOG_API_KEY is: $(echo ${CRUDDOG_API_KEY} | sed 's/./*/g')"
echo "CRUDDOG_APP_KEY is: $(echo ${CRUDDOG_APP_KEY} | sed 's/./*/g')"

DASHBOARD_ID=${1}

python cruddog/cruddog.py -b -i ${DASHBOARD_ID} | jq '. | del(.id,.modified,.created)' > ${DASHBOARD_ID}.json
