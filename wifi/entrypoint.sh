#!/bin/bash

sleep 15
CHECK_FREQ=300
VERBOSE="true"

while true; do
  wget --quiet --spider --no-check-certificate https://www.google.com
  RESULT=$?
  if [[ ${RESULT} -eq 0 ]] && [[ "${VERBOSE}" == "true" ]]; then
    echo "Your device is already connected to the internet."
    echo "Skipping setting up wifi-connect access point."
    echo "Will check again every ${CHECK_FREQ} seconds."
    echo "Going on mute now..."
    VERBOSE="false"
  elif [[ ${RESULT} -ne 0 ]]; then
    echo "Your device is not connected to the internet."
    echo "Starting up wifi-connect."
    echo "Connect to the access point and configure the SSID and passphrase for the network to connect to."
    VERBOSE="true"
    /app/wifi-connect -u /app/ui
  fi
  sleep "${CHECK_FREQ}"
done
