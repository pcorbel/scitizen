# -*- coding: utf-8 -*-

import time
from dataclasses import dataclass

import schedule
from balena.operator import Operator as Balena
from boinc.operator import Operator as Boinc
from scitizen.operator import Operator as Scitizen


@dataclass
class App:
    """The App is used to schedule and orchestrate the
    interactions between the BOINC client and the Scitizen API.

    Attributes:
        balena: The Balena operator.
        boinc: The BOINC operator.
        scitizen: The Scitizen operator.

    Methods:
        job: Run the tasks needed to synchronize the BOINC client with the Scitizen API.
    """

    balena: Balena = Balena()
    boinc: Boinc = Boinc()
    scitizen: Scitizen = Scitizen()

    def __post_init__(self) -> None:
        """Initialize the App.

        Seed the project table, check the hostname, set the schedule interval and
        run the agent
        """
        self.scitizen.set_projects()
        self.balena.set_hostname("scitizen")

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
        self.scitizen.clean_tasks()


if __name__ == "__main__":
    app: App = App()
