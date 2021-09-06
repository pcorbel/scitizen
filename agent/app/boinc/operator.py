# -*- coding: utf-8 -*-

import os
import socket
from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import Any, Dict, List

import boinc.utils as utils
from jinja2 import Template
from xmltodict import parse


@dataclass
class Operator:
    """The Operator is used to interact with the BOINC client.

    The operator is connected to the BOINC client via RPC, and is
    used to execute queries against the BOINC client database.

    Attributes:
        host: The name of the BOINC client host.
        port: The port of the BOINC client host.
        queries_dir: The directory where RPC query templates are stored.
        sock: The web socket used to connect via RPC.

    Methods:
        get_tasks: Fetch all the running tasks.
        get_host_info: Fetch all the info relative to the BOINC client host.
        sync_projects: Sync the user's enrolment on Scitizen projects.
    """

    host: str = "localhost"
    port: int = 31416
    queries_dir: str = str((Path(__file__).parent / "queries").resolve())
    sock: socket.socket = socket.socket()

    def __post_init__(self) -> None:
        """Initialize the Operator.

        Connect the socket to the BOINC client and authenticate against it
        in order to be ready to communicate with it via RPC.
        """

        self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP
        )
        self.sock.connect((self.host, self.port))
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate against the BOINC client.

        The first request is used to get the nonce.
        The second one is used to hash the concatenation of the nonce and the password.

        Official documentation is available
        `here <https://boinc.berkeley.edu/trac/wiki/GuiRpcProtocol#Authentication>`.
        """

        reply = self._send_request("auth1")
        nonce = utils.deep_get(reply, "boinc_gui_rpc_reply.nonce")
        digest = md5(nonce.encode()).hexdigest()
        self._send_request("auth2", data={"digest": digest})

    def _send_request(self, name: str, data: dict = None) -> Dict[str, Any]:
        """Send a query against the BOINC client.

        It is used to read a query template and render it.
        The goal is to be able to generate dynamic queries to be send against
        the BOINC client database.

        Args:
          name:
            The name of the request template.
          data:
            An optional dictionary of data used to render the template.

        Returns:
          The BOINC client answer.
        """

        with open(f"{self.queries_dir}/{name}.xml.j2") as file:
            template = Template(file.read())
        text = template.render(data=data)
        request = str(text) + "\003"

        self.sock.sendall(request.encode())

        stream = ""
        while True:
            buffer = self.sock.recv(8192).decode()
            stop = buffer.find("\003")
            if not stop == -1:
                break
            stream += buffer

        stream = stream + buffer[:stop]

        reply = parse(stream)
        return reply

    def get_tasks(self) -> List[Dict[str, Any]]:
        """Fetch all the running tasks.

        The raw answer from the BOINC client is formatted in-flight
        to be compatible with the Scitizen API.

        Returns:
          The list of running tasks.
        """

        # fetch data from the BOINC client and parse it
        reply = self._send_request(name="get_results")
        results = utils.deep_get(reply, "boinc_gui_rpc_reply.results.result")

        # skip if no results is found
        if results is None:
            return []

        # hack to handle edge case when there is only one task: set it in a list
        if isinstance(results, dict):
            results = [results]

        # iterate over all results
        tasks: list = []
        for result in results:
            task: dict = {}

            # generate a uuid for the task
            task.update({"uuid": utils.md5(result.get("name"))})

            # replace code state per human readable state
            task.update({"state": utils.get_result_state(result.get("state"))})

            # add task generic data
            task.update({"name": result.get("name")})
            task.update({"wu_name": result.get("wu_name")})
            task.update({"project_url": result.get("project_url")})
            task.update({"platform": result.get("platform")})
            task.update({"exit_code": result.get("exit_status")})
            task.update(
                {"exit_statement": utils.get_exit_statement(result.get("exit_status"))}
            )

            task.update(
                {"received_at": utils.to_isoformat(result.get("received_time"))}
            )
            task.update(
                {
                    "report_deadline_at": utils.to_isoformat(
                        result.get("report_deadline")
                    )
                }
            )
            task.update({"version_num": result.get("version_num")})
            task.update({"plan_class": result.get("plan_class")})
            task.update(
                {
                    "estimated_cpu_time_remaining": result.get(
                        "estimated_cpu_time_remaining"
                    )
                }
            )

            task.update(
                {"completed_at": utils.to_isoformat(result.get("completed_time"))}
            )

            # only if task is active
            active_task = result.get("active_task")
            if active_task is not None:
                # replace state code per human readable state
                task.update(
                    {
                        "active_task_state": utils.get_active_task_state(
                            active_task.get("active_task_state")
                        )
                    }
                )

                # replace scheduler state code per human readable state
                task.update(
                    {
                        "scheduler_state": utils.get_scheduler_state(
                            active_task.get("scheduler_state")
                        )
                    }
                )

                # add generic active task data
                task.update({"fraction_done": active_task.get("fraction_done")})
                task.update({"current_cpu_time": active_task.get("current_cpu_time")})
                task.update({"elapsed_time": active_task.get("elapsed_time")})
                task.update({"app_version_num": active_task.get("app_version_num")})
                task.update({"slot": active_task.get("slot")})
                task.update({"slot_path": active_task.get("slot_path")})
                task.update({"pid": active_task.get("pid")})
                task.update({"swap_size": active_task.get("swap_size")})
                task.update({"set_size": active_task.get("working_set_size_smoothed")})
                task.update({"page_fault_rate": active_task.get("page_fault_rate")})
                task.update({"bytes_sent": active_task.get("bytes_sent")})
                task.update({"bytes_received": active_task.get("bytes_received")})
                task.update({"progress_rate": active_task.get("progress_rate")})
                task.update(
                    {"checkpoint_cpu_time": active_task.get("checkpoint_cpu_time")}
                )

            # add final task to objects list
            tasks.append(task)

        return tasks

    def get_old_tasks(self) -> List[Dict[str, Any]]:
        """Fetch all the finished tasks still present in the BOINC client database.
        The raw answer from the BOINC client is formatted in-flight
        to be compatible with the Scitizen API.
        Returns:
          The list of finished tasks.
        """

        # fetch data from the BOINC client and parse it
        reply = self._send_request(name="get_old_results")
        results = utils.deep_get(reply, "boinc_gui_rpc_reply.old_results.old_result")

        # skip if no results is found
        if results is None:
            return []

        # hack to handle edge case when there is only one task: set it in a list
        if isinstance(results, dict):
            results = [results]

        # iterate over all results
        tasks: list = []
        for result in results:
            task: dict = {}

            # generate a uuid for the task
            task.update({"uuid": utils.md5(result.get("result_name"))})

            # add some generic data
            task.update({"active_task_state": "EXITED"})
            task.update({"current_cpu_time": result.get("cpu_time")})
            task.update(
                {"completed_at": utils.to_isoformat(result.get("completed_time"))}
            )
            task.update({"estimated_cpu_time_remaining": 0})
            task.update({"exit_code": result.get("exit_status")})
            task.update(
                {"exit_statement": utils.get_exit_statement(result.get("exit_status"))}
            )
            task.update({"elapsed_time": result.get("elapsed_time")})
            if int(result.get("exit_status")) == 0:
                task.update({"fraction_done": 1})

            # add final task to objects list
            tasks.append(task)

        return tasks

    def get_host_info(self) -> Dict[str, Any]:
        """Fetch all the info relative to the BOINC client host.

        The raw answer from the BOINC client is formatted in-flight
        to be compatible with the Scitizen API.

        Returns:
          The info on the BOINC client host.
        """

        # initialize the host info
        host: dict = {}

        # fetch data from the BOINC client and parse it
        reply = self._send_request(name="get_host_info")
        result = utils.deep_get(reply, "boinc_gui_rpc_reply.host_info")

        # hack to handle no results
        if result is None:
            result = {}

        # add static data relative to the hardware
        host.update({"uuid": os.getenv("BALENA_DEVICE_UUID")})
        host.update({"name": os.getenv("BALENA_DEVICE_NAME_AT_INIT")})
        host.update({"type": os.getenv("BALENA_DEVICE_TYPE")})
        host.update({"arch": os.getenv("BALENA_DEVICE_ARCH")})
        host.update({"operating_system_version": os.getenv("BALENA_HOST_OS_VERSION")})

        host.update({"cpid": result.get("host_cpid")})
        host.update({"cpu_type": result.get("p_model")})
        host.update({"cpu_architecture": result.get("p_vendor")})
        host.update({"cpu_features": result.get("p_features")})
        host.update({"processor_count": int(result.get("p_ncpus"))})
        host.update({"coprocessor_count": int(result.get("n_usable_coprocs"))})
        host.update({"product_name": result.get("product_name")})

        # add data relative to the software
        host.update({"floating_point_speed": float(result.get("p_fpops"))})
        host.update({"integer_speed": float(result.get("p_iops"))})
        host.update({"total_disk_space": float(result.get("d_total"))})
        host.update({"free_disk_space": float(result.get("d_free"))})
        host.update({"swap_space": float(result.get("m_swap"))})
        host.update({"domain_name": result.get("domain_name")})

        # fetch data from the BOINC client and parse it
        reply = self._send_request(name="exchange_versions")
        result = utils.deep_get(reply, "boinc_gui_rpc_reply.server_version")

        # hack to handle no results
        if result is None:
            result = {}

        # add static data relative to the software
        host.update(
            {
                "boinc_version": f"{result.get('major')}.{result.get('minor')}.{result.get('release')}"
            }
        )

        return host

    def sync_projects(self, projects: List[Dict[str, Any]]) -> None:
        """Sync the user's enrolment on projects.

        It is used to handle data coming from the Scitizen API and checks if
        the user still want to actively participate in a specific project.
        If yes, it will ensure that the BOINC client is attached to the project.
        Else, it will ensure that the BOINC client is detached from the project.

        Args:
          projects:
            The list of projects and all their related properties (including `is_active`)
            fetched from the Scitizen API.

        """

        # fetch data from the BOINC client and parse it
        reply = self._send_request(name="get_project_status")
        attached_projects = utils.deep_get(
            reply, "boinc_gui_rpc_reply.projects.project"
        )

        # hack to handle no results
        if attached_projects is None:
            attached_projects = []

        # hack to handle one result: set it in a list
        if isinstance(attached_projects, dict):
            attached_projects = [attached_projects]

        # extract project urls
        attached_projects_url = []
        for project in attached_projects:
            attached_projects_url.append(project.get("master_url"))

        # iterate over projects and do something if need be
        for project in projects:
            is_active = project.get("is_active")

            # attach project
            if is_active and project.get("url") not in attached_projects_url:
                print(f"attaching to project: {project.get('name')}")
                self._send_request(name="project_attach", data=project)

            # detach project
            if project.get("url") in attached_projects_url and not is_active:
                print(f"detaching from project: {project.get('name')}")
                self._send_request(name="project_detach", data=project)
