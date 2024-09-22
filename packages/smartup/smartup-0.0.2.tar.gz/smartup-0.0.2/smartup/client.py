import os
import warnings

SMARTUP_SERVER = os.getenv("SMARTUP_SERVER_URL", "")

if not SMARTUP_SERVER:
    warnings.warn("SMARTUP_SERVER_URL environment variable is not set or empty. Please set it to use the SmartUp platform.", UserWarning)

class SmartUp:
    """
    SmartUp client for interacting with SmartUp agents and models.

    Attributes:
        server_url (str): The URL of the SmartUp server.
        openai_api_key (str): The OpenAI API key.
    """

    def __init__(
        self,
        server_url=f"{SMARTUP_SERVER}/use-agent",
        openai_api_key="",
    ):
        self.server_url = server_url
        self.openai_api_key = openai_api_key
