"""
Modules to handle tasks.
For more details, see firedust.agency._base
"""

from typing import Dict, List

from firedust._utils.api import APIClient
from firedust._utils.types.agency import ScheduledTask
from firedust._utils.types.assistant import AssistantConfig


class Task:
    """
    Combine and exercise abilities to perform tasks.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (APIClient): The API client.
        schedule (Schedule): Tasks scheduler.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Task class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        # configuration
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

        # schedule
        self.schedule: Schedule = Schedule(config, api_client)

    def run(self, task: str) -> Dict[str, str]:
        """
        Runs a task.

        Args:
            task (str): The task to run.

        Returns:
            metadata (Dict[str, str]): The metadata of the created task.
        """
        response = self.api_client.post(
            f"assistant/{self.config.id}/agency/task/run",
            data={"task": task},
        )
        if not response.is_success:
            raise Exception(response.json()["message"])
        metadata: Dict[str, str] = response.json()

        return metadata


class Schedule:
    """
    Schedule and manage tasks to run at specific times.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Schedule class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

    def add(self, task: ScheduledTask) -> Dict[str, str]:
        """
        Adds a task to the schedule.

        Args:
            scheduled_task (ScheduledTask): The scheduled task.

        Returns:
            Dict[str, str]: Metadata of the scheduled task.
        """
        response = self.api_client.post(
            f"assistant/{self.config.id}/agency/task/schedule/add",
            data={"task": task},
        )

        if not response.is_success:
            raise Exception(response.json()["message"])

        metadata: Dict[str, str] = response.json()

        return metadata

    def list(self) -> List[ScheduledTask]:
        """
        Lists all scheduled tasks.

        Returns:
            List[ScheduledTask]: A list of scheduled tasks.
        """
        response = self.api_client.get(
            f"assistant/{self.config.id}/agency/task/schedule/list",
        )

        if not response.is_success:
            raise Exception(response.json()["message"])

        scheduled_tasks: List[ScheduledTask] = [
            ScheduledTask(**task) for task in response.json()["result"]
        ]
        return scheduled_tasks
