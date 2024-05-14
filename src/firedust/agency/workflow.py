"""
Module to handle workflows - sequences of tasks.

For more details, see: 
firedust.agency._base
firedust.agency.task
"""

from typing import Dict, List

from firedust.utils.api import APIClient
from firedust.utils.types.agency import WorkflowConfig
from firedust.utils.types.assistant import AssistantConfig


class Workflow:
    """
    Create workflows (sequences of tasks) and schedule them to run at specific times.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Workflow class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

    def run(self, workflow: WorkflowConfig) -> Dict[str, str]:
        """
        Creates and runs a workflow on a schedule.

        Args:
            workflow (WorkflowConfig): The workflow to create.

        Returns:
            metadata (Dict[str, str]): The metadata of the created workflow.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def list(self) -> List[WorkflowConfig]:
        """
        Lists all created workflows.

        Returns:
            List[WorkflowConfig]: A list of workflows.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def remove(self, workflow_id: str) -> Dict[str, str]:
        """
        Removes a workflow.

        Args:
            workflow_id (str): The id of the workflow to remove.

        Returns:
            metadata (Dict[str, str]): The metadata of the removed workflow.
        """
        raise NotImplementedError("This method is not implemented yet.")
