"""
Modules to handle tasks.
For more details, see firedust.agency._base
"""

from typing import Dict, List

from firedust.utils.api import SyncAPIClient
from firedust.utils.types.agency import ScheduledTask
from firedust.utils.types.assistant import AssistantConfig


class Task:
    """
    Combine and exercise abilities to perform tasks.

    Attributes:
        config (AssistantConfig): The assistant configuration.
        api_client (SyncAPIClient): The API client.
        schedule (Schedule): Tasks scheduler.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Task class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        # configuration
        self.config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client

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
        raise NotImplementedError("This method is not implemented yet.")


class Schedule:
    """
    Schedule and manage tasks to run at specific times.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Schedule class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client

    def add(self, task: ScheduledTask) -> Dict[str, str]:
        """
        Adds a task to the schedule.

        Args:
            scheduled_task (ScheduledTask): The scheduled task.

        Returns:
            Dict[str, str]: Metadata of the scheduled task.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def list(self) -> List[ScheduledTask]:
        """
        Lists all scheduled tasks.

        Returns:
            List[ScheduledTask]: A list of scheduled tasks.
        """
        raise NotImplementedError("This method is not implemented yet.")
