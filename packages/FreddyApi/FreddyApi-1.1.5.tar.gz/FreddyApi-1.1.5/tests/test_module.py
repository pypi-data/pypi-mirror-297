import unittest
from FreddyApi.module import FreddyApi, MessageRequestPayload, Message
from config import Config

class TestFreddyApi(unittest.TestCase):

    def setUp(self):
        # Load a real API token from your config
        token = Config.load_token()
        self.api = FreddyApi(token)

    def test_send_message_success(self):
        # Create the payload with real data
        payload = MessageRequestPayload(
            organization_id=1,  # Real organization ID
            assistant_id=15,    # Real assistant ID
            model="gpt-4o",     # Model name (e.g., gpt-4o)
            messages=[Message(content="Hello", role="user")]
        )

        # Perform a real API call
        try:
            response = self.api.create_run(payload)  # Assuming this function sends the message
            self.assertIsNotNone(response, "The response should not be None")
            print("API Response:", response)
        except Exception as e:
            self.fail(f"API call failed: {e}")

    def test_send_message_failure(self):
        # Create an invalid payload that should fail (example: invalid assistant ID)
        payload = MessageRequestPayload(
            organization_id=1,  # Real organization ID
            assistant_id=9999,  # Invalid assistant ID to simulate failure
            model="gpt-4o",     # Model name (e.g., gpt-4o)
            messages=[Message(content="Hello", role="user")]
        )

        # Perform a real API call and expect failure
        with self.assertRaises(Exception) as context:
            self.api.create_run(payload)  # Assuming this function sends the message

        self.assertIn("API request failed", str(context.exception))

    def test_check_run_status_completed(self):
        # Use real organization_id, run_key, and thread_key from a previous run
        organization_id = 1  # Real organization ID
        run_key = "run_zYJ14m8sGAqt7JBZ3NzVUaiu"  # Replace with a valid run_key
        thread_key = "thread_3T6BSDLITANwaGIkWaychThJ"  # Replace with a valid thread_key

        # Perform a real API call to check the run status
        try:
            status = self.api.check_run_status(organization_id=organization_id, run_key=run_key, thread_key=thread_key)
            self.assertEqual(status, "completed", "Run status should be completed")
            print("Run Status:", status)
        except Exception as e:
            self.fail(f"API call failed: {e}")

    def test_get_run_response(self):
        # Use real organization_id and thread_key from a previous run to get the response
        organization_id = 1              # Real organization ID
        thread_key = "real_thread_key"    # Replace with a valid thread_key

        # Perform a real API call to get the final run response
        try:
            response = self.api.get_run_response(organization_id=organization_id, thread_key=thread_key)
            self.assertIsNotNone(response, "The response should not be None")
            self.assertIn("text", response, "The response should contain the 'text' key")
            print("Run Response:", response["text"])
        except Exception as e:
            self.fail(f"API call failed: {e}")

    def test_execute_run_live(self):
        # Create a sample payload
        messages = [
            Message(content="Tell me a joke.", role="user"),
        ]
        payload = MessageRequestPayload(
            organization_id=1,            # Real organization ID
            assistant_id=2,               # Real assistant ID
            model="gpt-4o",               # Model name (e.g., gpt-4o)
            instructions="Provide a joke",
            additional_instructions="Use humor",
            messages=messages
        )

        # Perform the full live run, checking the status and getting the response
        try:
            response = self.api.execute_run(payload)
            self.assertIsNotNone(response, "The API response should not be None")
            self.assertIn("text", response, "The response should contain the 'text' key")

            # Print the final response
            print("Final Response:", response["text"])
        except Exception as e:
            self.fail(f"API call failed: {e}")


if __name__ == "__main__":
    unittest.main()