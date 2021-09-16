# -*- coding: utf-8 -*-

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import requests
import utils
import xmltodict
import yaml


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
        config: The path to the config file.

    Methods:
        set_device: Set the device info
        set_tasks: Set all the running tasks.
        clean_tasks: Run maintenance queries on the database.
        get_projects: Fetch all the projects available.
        set_projects: Set all the BOINC projects.
    """

    base_url: str = ""
    protocol: str = "http"
    host: str = "localhost"
    port: int = 8080
    session: requests.Session = requests.Session()
    config: str = f"{(Path(__file__).parent).resolve()}/projects.yml"

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

        self.session.post(
            url=f"{self.base_url}/devices/{device.get('uuid')}", json=device
        )

    def set_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Send tasks to the Scitizen API.

        It is used to update the Scitizen data with data coming from the BOINC Client.

        Args:
          tasks:
            The list of tasks to send to the Scitizen API.
        """

        for task in tasks:
            self.session.post(
                url=f"{self.base_url}/tasks/{task.get('uuid')}", json=task
            )

    def clean_tasks(self) -> None:
        """Send maintenance order to the Scitizen API.

        It is used to run maintenance queries on the database.
        """

        self.session.put(url=f"{self.base_url}/tasks/clean")

    def get_projects(self) -> List[str]:
        """Fetch projects from the Scitizen API.

        It is used to fetch the projects configuration coming from
        the Scitizen API in order to sync them locally.

        Returns:
          The list of projects coming from the Scitizen API.
        """

        return self.session.get(url=f"{self.base_url}/projects").json()

    def set_projects(self) -> None:
        """Send projects to the Scitizen API.

        It is used to fetch the official project list from the BOINC API,
        complete them with some Scitizen relative configs (like avatars and weak authenticators)
        and send them to the Scitizen API for persistence.
        """

        # load scitizen config
        with open(self.config) as file:
            config = yaml.load(file, Loader=yaml.SafeLoader).get("projects")

        # fetch official project list
        response = requests.get("https://boinc.berkeley.edu/project_list.php")
        projects = xmltodict.parse(response.text).get("projects").get("project")

        # iterate over official project and override config
        for project in projects:
            uuid: str = utils.md5(project.get("id"))
            project.update({"uuid": uuid})
            project.update({"platforms": str(project.get("platforms").get("name"))})
            project.update({"avatar": config.get(uuid, {}).get("avatar")})
            project.update(
                {"weak_authenticator": config.get(uuid, {}).get("weak_authenticator")}
            )

        for project in projects:
            self.session.post(
                url=f"{self.base_url}/projects/{project.get('uuid')}", json=project
            )
