import time
import requests
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict
import logging

# Setup basic logging
log = logging.getLogger(__name__)

@dataclass
class Message:
    content: str  # The content of the message
    role: str  # The role of the message author, 'user' or 'assistant'
    type: str = "text"  # Default to "text", but can be overridden

    def __post_init__(self):
        # Validate the role
        if self.role not in ["user", "assistant"]:
            raise ValueError("role must be either 'user' or 'assistant'")

        # Validate the type
        if self.type not in ["text", "other_allowed_type"]:  # Adjust allowed types if necessary
            raise ValueError("type must be 'text' or any other allowed type")

@dataclass
class MessageRequestPayload:
    userId: Optional[int] = None  # Optional user ID
    assistantId: Optional[int] = None  # Optional assistant ID
    threadId: Optional[str] = None  # Optional thread ID
    model: Optional[str] = None  # Optional model, e.g., "gpt-4o"
    messages: List[Message] = field(default_factory=list)  # List of Message objects
    stream: bool = False  # Option for streaming response, default to False
    frequency_penalty: float = 0.0  # Defaults to 0
    n: int = 1  # Number of responses, default to 1
    presence_penalty: float = 0.0  # Defaults to 0
    response_format: str = "text"  # Defaults to "text"
    temperature: float = 1.0  # Temperature for creativity, default to 1
    top_p: float = 1.0  # Nucleus sampling probability, default to 1
    toolIds: Optional[List[str]] = None  # Optional list of tool IDs
    additionalTools: Optional[List[str]] = None  # Optional list of additional tools
    files: Optional[List[str]] = None  # Optional list of uploaded file IDs
    instructions: Optional[str] = None  # Optional main instructions for the assistant
    additionalInstructions: Optional[str] = None  # Optional extra instructions

    def to_dict(self) -> Dict:
        """
        Convert the dataclass to a dictionary, removing any None values.
        This ensures the payload sent to the API is clean and well-formed.
        """
        payload = {
            "userId": self.userId,
            "assistantId": self.assistantId,
            "threadId": self.threadId,
            "model": self.model,
            "messages": [msg.__dict__ for msg in self.messages],  # Convert message objects to dictionaries
            "stream": self.stream,
            "frequency_penalty": self.frequency_penalty,
            "n": self.n,
            "presence_penalty": self.presence_penalty,
            "response_format": self.response_format,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "toolIds": self.toolIds,
            "additionalTools": self.additionalTools,
            "files": self.files,
            "instructions": self.instructions,
            "additionalInstructions": self.additionalInstructions
        }
        # Remove any keys with None values to avoid sending unnecessary data
        return {k: v for k, v in payload.items() if v is not None}

class FreddyApi:
    BASE_URLS = {
        "v1": "https://freddy-core-api.azurewebsites.net/v1"
    }

    def __init__(self, token: str, version: str = "v1"):
        """
        Initialize the FreddyApi class with the authentication token and API version.

        :param token: The Bearer token for authentication
        :param version: The API version to use (default is v2)
        """
        if version not in self.BASE_URLS:
            raise ValueError(f"Unsupported API version: {version}. Supported versions are: {list(self.BASE_URLS.keys())}")

        self.token = token
        self.version = version
        self.base_url = self.BASE_URLS[version]
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.rate_limit_reached = False

    def create_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
        """
        Send a message to a specific assistant via the /messages endpoint.

        :param payload: A MessageRequestPayload object containing the request data
        :return: Response from the API or an error message if the request fails
        """
        if self.rate_limit_reached:
            log.error("Rate limit reached. Please try again later.")
            raise Exception("Rate limit reached, please try again later.")

        url = f"{self.base_url}/messages"
        data = payload.to_dict()

        try:
            # Send POST request to the /messages endpoint
            log.debug(f"Sending request to {url} with payload: {data}")
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 200:
                log.debug("API response received successfully.")
                self.rate_limit_reached = True  # Simulate rate limit being reached after a successful request
                return response.json()
            else:
                # Handle non-200 responses and log errors
                try:
                    error_message = response.json().get("error", response.text)
                except ValueError:
                    error_message = response.text  # Fallback to raw text if JSON decoding fails
                log.error(f"API request failed with status {response.status_code}: {error_message}")
                raise Exception(f"API request failed with status {response.status_code}: {error_message}")

        except requests.RequestException as e:
            # Handle request exceptions, e.g., network issues
            log.error(f"An error occurred during the API request: {str(e)}")
            raise Exception(f"An error occurred during the API request: {str(e)}")

    def check_run_status(self, run_key: str, thread_key: str) -> str:
        """
        Continuously check the run status for the process until it reaches a terminal state.

        :param run_key: The run key to track the process
        :param thread_key: The thread key associated with the process
        :return: Final status when process is completed or an error state
        """
        url_status = f"{self.base_url}/messages/run-status"
        payload = {
            "organization_id": 2,  # Customize based on the actual organization_id used
            "thread_key": thread_key,
            "run_key": run_key
        }

        non_terminal_statuses = ["queued", "in_progress", "requires_action", "cancelling"]
        error_statuses = ["cancelled", "failed", "incomplete", "expired"]

        while True:
            try:
                log.debug(f"Checking run status for run_key: {run_key}, thread_key: {thread_key}")
                response = requests.get(url_status, params=payload)

                if response.status_code == 200:
                    response_data = response.json()
                    run_status = response_data.get("runStatus", "unknown")

                    log.info(f"Current run status: {run_status}")

                    if run_status == "completed":
                        log.info("Process completed successfully.")
                        return "completed"
                    elif run_status in error_statuses:
                        log.error(f"Process failed with status: {run_status}")
                        return run_status
                    elif run_status in non_terminal_statuses:
                        log.info(f"Process still in progress: {run_status}. Retrying in 10 seconds...")
                        time.sleep(1)
                    else:
                        log.error(f"Unknown run status: {run_status}. Exiting.")
                        return "unknown"

                else:
                    log.error(f"Failed to retrieve run status. HTTP Status Code: {response.status_code}")
                    return "error"

            except requests.RequestException as e:
                log.error(f"Error while checking run status: {e}")
                return "error"

    def get_run_response(self, organization_id: int, thread_key: str) -> Union[Dict, None]:
        """
        Retrieve the run response from the API.

        :param organization_id: The organization ID
        :param thread_key: The thread key to track the process
        :return: The run response (e.g., text) or an error message
        """
        url = f"{self.base_url}/messages/run-response"
        payload = {"organization_id": organization_id, "thread_key": thread_key}

        try:
            response = requests.get(url, headers=self.headers, params=payload)
            if response.status_code == 200:
                return response.json()
            else:
                error_message = response.json().get("error", response.text)
                raise Exception(f"Failed to get run response: {error_message}")
        except requests.RequestException as e:
            raise Exception(f"Error occurred: {e}")