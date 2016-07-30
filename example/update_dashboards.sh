#!/usr/bin/env bash
set -uex
set -o pipefail


# Check our variables are correctly configured
echo "CRUDDOG_API_KEY is: $(echo ${CRUDDOG_API_KEY} | sed 's/./*/g')"
echo "CRUDDOG_APP_KEY is: $(echo ${CRUDDOG_APP_KEY} | sed 's/./*/g')"

TEMP_FILE=temp.json

for DASHBOARD_FILE in $(ls -1 *.json); do
  echo "Processing dashboard ${DASHBOARD_FILE}"

  DASHBOARD_ID=$(echo ${DASHBOARD_FILE} | grep -Eo '(^[0-9]*)')

  # Dump out the current dashboard, minus some unnecessary fields for comparison
  python cruddog/cruddog.py -b -i ${DASHBOARD_ID} | jq '. | del(.id,.modified,.created)' > ${TEMP_FILE}

  if $(diff -q ${DASHBOARD_FILE} ${TEMP_FILE} > /dev/null); then
    echo "No changes required for ${DASHBOARD_ID}, skipping!"
  else
    echo "Updating dashboard ${DASHBOARD_ID}"
    python cruddog/cruddog.py -u -i ${DASHBOARD_ID} < ${DASHBOARD_FILE}
  fi

  rm ${TEMP_FILE}
done
