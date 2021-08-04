# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Any, Dict, List

import requests


@dataclass
class Operator:
    """The Operator is used to interact with the Scitizen API.

    The operator is connected to the Scitizen API via REST, and is
    used to fetch and send data to the API.

    Attributes:
        base_url: The base url of the Scitizen API endpoint.
        protocol: The protocol used to connect to the Scitizen REST API.
        host: The name of the Scitizen API host.
        port: The port of the Scitizen API host.
        session: A session to improve performance.

    Methods:
        set_device: Set the device info
        set_tasks: Set all the running tasks.
        get_projects: Fetch all the projects available.
        set_projects: Set the state (enabled/disabled) of all the projects available.
    """

    base_url: str = ""
    protocol: str = "http"
    host: str = "localhost"
    port: int = 8080
    session: requests.Session = requests.Session()

    def __post_init__(self) -> None:
        """Initialize the Operator.

        Setup the base url of the API and open-up a session.
        """

        self.base_url = f"{self.protocol}://{self.host}:{self.port}/api"

    def set_device(self, device: Dict[str, Any]) -> None:
        """Send device to the Scitizen API.

        It is used to update the Scitizen data with data coming from the BOINC Client.

        Args:
          device:
            The device data to send to the Scitizen API.
        """

        self.session.post(url=f"{self.base_url}/device/{device.get('id')}", json=device)

    def set_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Send tasks to the Scitizen API.

        It is used to update the Scitizen data with data coming from the BOINC Client.

        Args:
          tasks:
            The list of tasks to send to the Scitizen API.
        """

        for task in tasks:
            self.session.post(url=f"{self.base_url}/task/{task.get('id')}", json=task)

    def get_projects(self) -> List[str]:
        """Send tasks to the Scitizen API.

        It is used to fetch the projects configuration coming from
        the Scitizen API in order to sync them locally.

        Returns:
          The list of projects coming from the Scitizen API.
        """

        return self.session.get(url=f"{self.base_url}/projects").json()

    def set_projects(self, projects: List[Dict[str, Any]]) -> None:
        """Send projects to the Scitizen API.

        It is used to update the Scitizen data with data coming from the BOINC Client.

        Args:
          projects:
            The list of projects to send to the Scitizen API.
        """

        for project in projects:
            self.session.post(
                url=f"{self.base_url}/project/{project.get('id')}", json=project
            )
