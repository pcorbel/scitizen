#!/bin/sh

export DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
export PORTAL_SSID=Scitizen
export PORTAL_LISTENING_PORT=8000
export FREQ=120

while true; do
  echo "Checking internet connectivity ..."
  wget --spider --no-check-certificate 1.1.1.1 > /dev/null 2>&1
  RESULT=$?
  if [ ${RESULT} -eq 0 ]; then
    echo "Your device is already connected to the internet."
    echo "Skipping setting up Wifi-Connect Access Point. Will check again in ${FREQ} seconds"
  else
    echo "Your device is not connected to the internet."
    echo "Starting up Wifi-Connect."
    echo "Connect to the Access Point and configure the SSID and Passphrase for the network to connect to."
    /app/wifi-connect -u /app/ui
  fi
  sleep ${FREQ}
done
