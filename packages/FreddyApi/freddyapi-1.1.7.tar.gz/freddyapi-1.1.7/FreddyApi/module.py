import time
import requests
from dataclasses import dataclass, field
from typing import List, Optional, Union, Dict
import logging
import httpx
import regex as re
import json

# Setup basic logging
logging.basicConfig(level=logging.INFO)  # You can change this to INFO or ERROR for less verbosity
log = logging.getLogger(__name__)
json_pattern = re.compile(r'\{[^{}]*\}|\[[^\[\]]*\]')

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
    organization_id: int = 0  # Organization ID
    assistant_id: int = 0  # Assistant ID
    thread_id: Optional[int] = None  # Thread ID, optional
    model: Optional[str] = None  # Model used, optional, defaults to None
    instructions: Optional[str] = None  # Instructions for the assistant, optional
    additional_instructions: Optional[str] = None  # Additional instructions for the assistant, optional
    messages: List[Message] = field(default_factory=list)  # List of Message objects

    def to_dict(self) -> Dict:
        """
        Convert the dataclass to a dictionary, removing any None values.
        This ensures the payload sent to the API is clean and well-formed.
        """
        payload = {
            "organization_id": self.organization_id,
            "assistant_id": self.assistant_id,
            "thread_id": self.thread_id,
            "model": self.model,
            "instructions": self.instructions,
            "additional_instructions": self.additional_instructions,
            "messages": [msg.__dict__ for msg in self.messages],  # Convert message objects to dictionaries
        }
        # Remove any keys with None values to avoid sending unnecessary data
        return {k: v for k, v in payload.items() if v is not None}


# Define a proper class to represent the structure of the streamed response
class StreamEvent:
    def __init__(self, event: str, status: Optional[str], is_response: bool, response: Optional[str], thread_id: int):
        self.event = event
        self.status = status
        self.is_response = is_response
        self.response = response
        self.thread_id = thread_id

    def __repr__(self):
        return f"<StreamEvent event={self.event} status={self.status} response={self.response} thread_id={self.thread_id}>"

    @classmethod
    def from_json(cls, data: dict):
        return cls(
            event=data.get("event"),
            status=data.get("status"),
            is_response=data.get("isResponse", False),
            response=data.get("response"),
            thread_id=data.get("threadId")
        )


def is_valid_json(data):
    """
    Check if a given string is a complete and valid JSON object.
    This method checks if there are balanced braces or brackets.
    """
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False


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
            raise ValueError(
                f"Unsupported API version: {version}. Supported versions are: {list(self.BASE_URLS.keys())}")

        self.token = token
        self.version = version
        self.base_url = self.BASE_URLS[version]
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.rate_limit_reached = False

    def create_stream(self, payload: "MessageRequestPayload", callback: callable) -> None:
        """
        Initiates a streaming API request that streams the response word by word over time.

        :param payload: A MessageRequestPayload object containing the request data
        :param callback: A callable function that processes each streamed StreamEvent object as it arrives
        """
        url = f"{self.base_url}/messages/run-stream"
        data = payload.to_dict()  # Convert payload to dictionary

        # Ensure token is properly formatted and stripped of extra spaces
        headers = {
            "Authorization": f"Bearer {self.token.strip()}",
            "Content-Type": "application/json"
        }

        try:
            # Increase the timeout for the client (e.g., 60 seconds)
            timeout = httpx.Timeout(60.0)  # Adjust this as necessary

            # Create an HTTPX client for streaming with increased timeout
            with httpx.Client(timeout=timeout) as client:
                with client.stream("POST", url, json=data, headers=headers) as response:

                    # Raise an error if the response status code is not 200
                    response.raise_for_status()

                    buffer = ""  # Buffer to accumulate chunks of data

                    # Iterate over the streamed response content
                    for chunk in response.iter_text():
                        buffer += chunk  # Append the chunk to the buffer

                        # Use regex to find all complete JSON objects or arrays in the buffer
                        matches = list(re.finditer(json_pattern, buffer))

                        if matches:  # Only process if there are matches
                            for match in matches:
                                json_str = match.group()  # Extract the matched JSON string

                                try:
                                    # Parse the extracted JSON
                                    json_data = json.loads(json_str)

                                    # Convert the JSON to a StreamEvent class instance (or handle as needed)
                                    event = StreamEvent.from_json(json_data)

                                    # Invoke the callback with the parsed event data
                                    callback(event)

                                except json.JSONDecodeError as e:
                                    log.error(f"Failed to decode JSON: {e}")

                            # Remove the matched portion from the buffer to prevent reprocessing
                            buffer = buffer[matches[-1].end():]

        except httpx.RequestError as e:
            log.error(f"Request failed: {e}")

    def create_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
        """
        Send a message to a specific assistant via the /messages endpoint.

        :param payload: A MessageRequestPayload object containing the request data
        :return: Response from the API or an error message if the request fails
        """
        if self.rate_limit_reached:
            log.error("Rate limit reached. Please try again later.")
            raise Exception("Rate limit reached, please try again later.")

        url = f"{self.base_url}/messages/run-create"
        data = payload.to_dict()

        try:
            # Send POST request to the /messages endpoint
            response = requests.post(url, headers=self.headers, json=data)

            if response.status_code == 200:
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

    def check_run_status(self, run_key: str, thread_key: str, organization_id: int) -> str:
        """
        Get the status of a run based on the run key and thread key.

        :param organization_id: The organization ID
        :param run_key: The run key to track the process
        :param thread_key: The thread key associated with the process
        :return: Final status when process is completed or an error state
        """
        url_status = f"{self.base_url}/messages/run-status"
        payload = {
            "organization_id": organization_id,
            "thread_key": thread_key,
            "run_key": run_key
        }

        try:
            response = requests.get(url_status, json=payload, headers=self.headers)

            if response.status_code == 200:
                response_data = response.json()
                run_status = response_data.get("runStatus", "unknown")

                return run_status

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
            response = requests.get(url, headers=self.headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                error_message = response.json().get("error", response.text)
                raise Exception(f"Failed to get run response: {error_message}")
        except requests.RequestException as e:
            raise Exception(f"Error occurred: {e}")

    def execute_run(self, payload: MessageRequestPayload) -> Union[Dict, None]:
        """
        Executes the entire run process:
        1. Creates a run (sends message payload).
        2. Polls for run completion.
        3. Returns the final run response.

        :param payload: A MessageRequestPayload object containing the request data.
        :return: The final run response (e.g., text) or an error message if the process fails.
        """
        non_terminal_statuses = ["queued", "in_progress", "requires_action", "cancelling"]
        error_statuses = ["cancelled", "failed", "incomplete", "expired"]

        try:
            # Step 1: Create the run
            response = self.create_run(payload)
            if not response:
                raise Exception("Failed to initiate run")

            run_key = response.get("runKey")
            thread_key = response.get("threadKey")

            status = ""

            attempts = 0
            while status != "completed":
                status = self.check_run_status(run_key, thread_key, payload.organization_id)
                if status in error_statuses:
                    raise Exception(f"Run failed with status: {status}")
                time.sleep(0.5)
                attempts += 1
                if attempts >= 10000:
                    log.warning("Max polling attempts reached")
                    break
            else:
                while status != "completed":
                    status = self.check_run_status(run_key, thread_key, payload.organization_id)
                    if status in error_statuses:
                        raise Exception(f"Run failed with status: {status}")
                    time.sleep(0.5)

            # Step 3: Get the final response
            return self.get_run_response(payload.organization_id, thread_key)

        except Exception as e:
            log.error(f"Error during the run process: {e}")
            return None
