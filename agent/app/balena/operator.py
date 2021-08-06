# -*- coding: utf-8 -*-

import os
from dataclasses import dataclass
from typing import Optional
import requests


@dataclass
class Operator:
    """The Operator is used to interact with the Balena Supervisor API.

    The operator is connected to the Supervisor API via REST, and is
    used to fetch and send data to the API.

    Attributes:
        supervisor_address: The base url of the Supervisor API.
        host_config_endpoint: The Supervisor endpoint to access the host config.
        reboot_endpoint: The Supervisor endpoint to reboot the device.
        supervisor_api_key: The API key to authenticate against the Supervisor.
        host_config_url: The full url to access the host config.
        reboot_url: The full url to reboot the device.
        session: A session to improve performance.

    Methods:
        get_hostname: Get the hostname.
        set_hostname: Set the hostname and reboot.
    """

    supervisor_address: Optional[str] = os.getenv("BALENA_SUPERVISOR_ADDRESS")
    host_config_endpoint: str = "/v1/device/host-config?apikey="
    reboot_endpoint: str = "/v1/reboot?apikey="
    supervisor_api_key: Optional[str] = os.getenv("BALENA_SUPERVISOR_API_KEY")
    host_config_url: str = ""
    reboot_url: str = ""
    session: requests.Session = requests.Session()

    def __post_init__(self) -> None:
        """Initialize the Operator.

        Setup the base urls of the API and open-up a session.
        """

        self.host_config_url = f"{self.supervisor_address}{self.host_config_endpoint}{self.supervisor_api_key}"
        self.reboot_url = (
            f"{self.supervisor_address}{self.reboot_endpoint}{self.supervisor_api_key}"
        )

    def get_hostname(self) -> Optional[str]:
        """Fetch hostname from the Supervisor API.

        It is used to fetch the current hostname coming from
        the Supervisor API in order to check if the hostname is correct.

        Returns:
          The current hostname
        """

        return (
            self.session.get(url=self.host_config_url)
            .json()
            .get("network")
            .get("hostname")
        )

    def set_hostname(self, hostname: str) -> None:
        """Send the hostname to the Supervisor API.

        It is used to update the hostname of the device.
        If need be, it will also reboot the device for the hostname to be flushed.

        Args:
          hostname:
            The hostname to be set on the device.
        """

        if not hostname == self.get_hostname():
            print(f"setting hostname to {hostname} and rebooting...")
            data: dict = {"network": {"hostname": hostname}}
            headers: dict = {"Content-Type": "application/json"}
            self.session.patch(url=self.host_config_url, json=data, headers=headers)
            self.session.post(url=self.reboot_url, headers=headers)
        else:
            print(f"hostname already set to {hostname}. skipping... ")
