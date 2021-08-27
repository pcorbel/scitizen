#!/bin/sh

sleep 15

while true; do
  echo "Checking internet connectivity ..."
  wget --quiet --spider --no-check-certificate https://www.google.com
  RESULT=$?
  if [ ${RESULT} -eq 0 ]; then
    echo "Your device is already connected to the internet."
    echo "Skipping setting up wifi-connect access point."
    echo "Will check again in ${CHECK_FREQ} seconds."
  else
    echo "Your device is not connected to the internet."
    echo "Starting up wifi-connect."
    echo "Connect to the access point and configure the SSID and passphrase for the network to connect to."
    /app/wifi-connect -u /app/ui
  fi
  sleep "${CHECK_FREQ}"
done
