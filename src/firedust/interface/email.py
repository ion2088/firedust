"""
Email interface module for the Firedust assistant.

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_NAME")

    # Deploy the assistant to email
    assistant.interface.email.deploy(email_config)

    # Chat with the assistant by sending an email to the given email address

    # Use email interface in custom workflows
    email = assistant.interface.email.compose("Write a detailed report on the meeting.")
    assistant.interface.email.send(to="team@fusionfuel.com", email=email)
"""

from firedust.utils.api import AsyncAPIClient, SyncAPIClient
from firedust.utils.types.assistant import AssistantConfig
from firedust.utils.types.interface import Email, EmailConfig


class EmailInterface:
    """
    A collection of methods to interact with the assistant on email.
    """

    def __init__(self, config: AssistantConfig, api_client: SyncAPIClient) -> None:
        """
        Initializes a new instance of the Email class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (SyncAPIClient): The API client.
        """
        self.assistant_config: AssistantConfig = config
        self.api_client: SyncAPIClient = api_client
        self.email_config: EmailConfig | None = None

    def compose(self, instruction: str) -> Email:
        """
        Assistant writes an email based on the given instruction.

        Args:
            instruction (str): The instruction for the assistant.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def send(self, to: str, email: Email) -> None:
        """
        Assistant sends an email.

        Args:
            to (str): The email address of the assistant.
            email (Email): The email to send.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def deploy(self, config: EmailConfig) -> None:
        """
        Deploys the assistant to email.

        Args:
            config (EmailConfig): The email configuration.
        """
        raise NotImplementedError("This method is not implemented yet.")


class AsyncEmailInterface:
    """
    A collection of methods to interact with the assistant on email asynchronously.
    """

    def __init__(self, config: AssistantConfig, api_client: AsyncAPIClient) -> None:
        """
        Initializes a new instance of the AsyncEmail class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (AsyncAPIClient): The API client.
        """
        self.assistant_config: AssistantConfig = config
        self.api_client: AsyncAPIClient = api_client
        self.email_config: EmailConfig | None = None

    async def compose(self, instruction: str) -> Email:
        """
        Assistant writes an email based on the given instruction.

        Args:
            instruction (str): The instruction for the assistant.
        """
        raise NotImplementedError("This method is not implemented yet.")

    async def send(self, to: str, email: Email) -> None:
        """
        Assistant sends an email.

        Args:
            to (str): The email address of the assistant.
            email (Email): The email to send.
        """
        raise NotImplementedError("This method is not implemented yet.")

    async def deploy(self, config: EmailConfig) -> None:
        """
        Deploys the assistant to email.

        Args:
            config (EmailConfig): The email configuration.
        """
        raise NotImplementedError("This method is not implemented yet.")
