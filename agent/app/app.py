# -*- coding: utf-8 -*-

import os
import time
from dataclasses import dataclass

import schedule
import yaml  # type: ignore
from boinc.operator import Operator as Boinc
from scitizen.operator import Operator as Scitizen


@dataclass
class App:
    """The App is used to schedule and orchestrate the
    interactions between the BOINC client and the Scitizen API.

    Attributes:
        boinc: The BOINC operator.
        scitizen: The Scitizen operator.

    Methods:
        job: Run the tasks needed to synchronize the BOINC client with the Scitizen API.
    """

    boinc: Boinc = Boinc()
    scitizen: Scitizen = Scitizen()

    def __post_init__(self) -> None:
        """Initialize the App.

        Seed the project table, set the schedule interval and
        run the agent
        """
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/projects.yml") as file:
            projects = yaml.load(file, Loader=yaml.SafeLoader).get("projects")
            self.scitizen.set_projects(projects)

        schedule.every(30).seconds.do(self.job)

        while True:
            schedule.run_pending()
            time.sleep(1)

    def job(self):
        """Synchronize the BOINC client with the Scitizen API.

        It will sync the projects attachments, sync the tasks,
        and sync the host data.
        """
        self.boinc.sync_projects(self.scitizen.get_projects())
        self.scitizen.set_tasks(self.boinc.get_tasks())
        self.scitizen.set_tasks(self.boinc.get_old_tasks())
        self.scitizen.set_device(self.boinc.get_host_info())


if __name__ == "__main__":
    app: App = App()
