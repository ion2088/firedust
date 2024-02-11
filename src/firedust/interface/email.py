"""
Email interface module for the Firedust assistant.

Example:
    import firedust

    assistant = firedust.assistant.load("ASSISTANT_ID")

    # Deploy the assistant to email
    assistant.interface.email.deploy(email_config)

    # Chat with the assistant by sending an email to the given email address

    # Use email interface in custom workflows
    email = assistant.interface.email.compose("Write a detailed report on the meeting.")
    assistant.interface.email.send(to="team@fusionfuel.com", email=email)
"""

from firedust._utils.api import APIClient
from firedust._utils.errors import EmailError
from firedust._utils.types.assistant import AssistantConfig
from firedust._utils.types.interface import Email, EmailConfig


class EmailInterface:
    """
    A collection of methods to interact with the assistant on email.
    """

    def __init__(self, config: AssistantConfig, api_client: APIClient) -> None:
        """
        Initializes a new instance of the Email class.

        Args:
            config (AssistantConfig): The assistant configuration.
            api_client (APIClient): The API client.
        """
        self.assistant_config: AssistantConfig = config
        self.api_client: APIClient = api_client
        self.email_config: EmailConfig | None = None

    def compose(self, instruction: str) -> Email:
        """
        Assistant writes an email based on the given instruction.

        Args:
            instruction (str): The instruction for the assistant.
        """
        response = self.api_client.post(
            f"assistant/{self.assistant_config.id}/interface/email/compose",
            data={"instruction": instruction},
        )

        if response.status_code != 200:
            raise EmailError("Failed to compose email.")

        return Email(**response.json()["data"])

    def send(self, to: str, email: Email) -> None:
        """
        Assistant sends an email.

        Args:
            to (str): The email address of the assistant.
            email (Email): The email to send.
        """
        response = self.api_client.post(
            f"assistant/{self.assistant_config.id}/interface/email/send",
            data={"to": to, "email": email.model_dump()},
        )

        if response.status_code != 200:
            raise EmailError("Failed to send email.")

    def deploy(self, config: EmailConfig) -> None:
        """
        Deploys the assistant to email.

        Args:
            config (EmailConfig): The email configuration.
        """

        response = self.api_client.post(
            f"assistant/{self.assistant_config.id}/interface/email/deploy",
            data={"email": config.model_dump()},
        )
        if response.status_code != 200:
            raise EmailError("Failed to deploy assistant to email.")

        self.email_config = config
        self.assistant_config.interfaces.email = self.email_config
