#!/bin/sh

# launch boinc in the background
service boinc-client start > /dev/null 2>&1

# wait for boinc srvice to be up and running
while true; do 
  service boinc-client status | grep "Status of BOINC core client: running." > /dev/null 2>&1
  RESULT=$?
  if [ ${RESULT} -eq 0 ]; then
    sleep 60
  else
    echo "BOINC core client is not started yet..."
    sleep 5
  fi
done
