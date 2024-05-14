"""
Module to configure and exercise agency.

Freedom to think, choose, combine and exercise abilities to perform
tasks and achieve goals. Accelerate growth and wellbeing of humanity.


Usage example:
    import firedust

    # Load an existing assistant
    assistant = firedust.assistant.load("ASSISTANT_NAME")

    # Run a task
    result = assistant.agency.task.run("Perform research of the latest feedback emails and send me a summary at john.doe@aviato.com")
    print(result)

    # Schedule a task
    result = assistant.agency.task.schedule.add(
        task="Perform research of the latest feedback emails and send me a summary at john.doe@aviato.com"
        schedule="every day at 9:00am EST"
    )
    print(result)

    # List scheduled tasks
    tasks = assistant.agency.task.schedule.list()
    print(tasks)

    # Remove a scheduled task
    assistant.agency.task.schedule.remove(task_id)

    # Create and run a workflow on a schedule
    # Workflow is a sequence of tasks that are executed in a specific order
    # and scheduled to run at a specific time.
    workflow = WorkflowConfig(
        name="Daily Feedback Summary",
        description="A daily summary of the latest feedback emails",
        tasks=[
            "Perform research of the latest feedback emails",
            "Send me a summary at john.doe@aviato.com",
            "Write a detailed report and send it to the team on Slack channel #feedback"
        ],
        schedule="every day at 9:00am EST",
    )
    result = assistant.agency.workflow.run(workflow)

    # List workflows
    workflows = assistant.agency.workflow.list()

    # Remove a workflow
    assistant.agency.workflow.remove(workflow_id)
"""

from firedust.agency.task import Task
from firedust.agency.workflow import Workflow
from firedust.utils.api import APIClient
from firedust.utils.types.assistant import AssistantConfig


class Agency:
    """
    Freedom to think, choose, combine and exercise abilities to perform tasks and workflows.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Agency class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.config: AssistantConfig = config
        self.api_client: APIClient = api_client

        self.task: Task = Task(config, api_client)
        self.workflow: Workflow = Workflow(config, api_client)
