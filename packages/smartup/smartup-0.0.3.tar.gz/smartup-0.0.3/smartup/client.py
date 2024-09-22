import os
import warnings
import requests
import uuid

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

    class chat:
        """
        A nested class for interacting with the chat functionality of the SmartUp agent.
        """

        @staticmethod
        def create(
            agent,
            messages,
            model="gpt-4",
            email=None,
            hyperparameters=None,
            conversation_id="",
            custom_deployment="",
            response_format=None,
        ):
            """
            Creates a chat conversation with the SmartUp agent.

            Args:
                agent (str): The name of the agent.
                messages (list): A list of messages exchanged in the conversation.
                model (str): The model to use for the conversation (default is "gpt-4"). Can be "gpt-3.5" or "gpt-4".
                email (str): The email associated with the conversation.
                hyperparameters (dict): Additional hyperparameters for the conversation.
                conversation_id (str): The ID of the conversation.

            Returns:
                str: The response from the SmartUp agent.
            """
            
            data = {
                "conversationId": conversation_id or f"smartup-sdk-{str(uuid.uuid4())}",
                "messages": messages,
                "agentName": agent,
                "email": email or "module@smartup.lat",
                "model": model,
                "hyperparameters": hyperparameters or {},
                "customDeployment": custom_deployment,
                "responseFormat": response_format,
            }
            response = requests.post(
                f"{SMARTUP_SERVER}/use-agent",
                json=data,
                headers={"Content-Type": "application/json"},
            )
            return response.text.replace("[DONE]", "")

        @staticmethod
        def create_batch(
            agent,
            conversations,
            model="gpt-4",
            email=None,
            hyperparameters=None,
            custom_deployment="",
            response_format=None,
        ):
            """
            Creates multiple chat conversations with the SmartUp agent.

            Args:
                agent (str): The name of the agent.
                conversations (list): A list of dictionaries, each containing messages and conversation_id.
                model (str): The model to use for the conversation (default is "gpt-4"). Can be "gpt-3.5" or "gpt-4".
                email (str): The email associated with the conversation.
                hyperparameters (dict): Additional hyperparameters for the conversation.
            Returns:
                list: A list of responses from the SmartUp agent.
            """
            responses = []
            print(f"Sample Messages: {type(conversations[0]['messages'])}")
            for conversation in conversations:
                messages = conversation.get("messages", [])
                data = {
                    "conversation_id": conversation.get("conversation_id", ""),
                    "messages": messages,
                    "agent_name": agent,
                    "email": email or "module@smartup.lat",
                    "model": model,
                    "hyperparameters": hyperparameters or {},
                    "custom_deployment": custom_deployment,
                    "response_format": response_format,
                }
                response = requests.post(
                    f"{SMARTUP_SERVER}/use-agent",
                    json=data,
                    headers={"Content-Type": "application/json"},
                )
                responses.append(response.text.replace("[DONE]", ""))
            return responses

