import unittest
from unittest.mock import patch
from FreddyApi.module import FreddyApi, MessageRequestPayload, Message
from config import Config

class TestFreddyApi(unittest.TestCase):

    def setUp(self):
        # Set up an instance of FreddyApi with a dummy token
        self.api = FreddyApi(token=Config.load_token())

    @patch("FreddyApi.module.requests.post")
    def test_send_message_success(self, mock_post):
        # Mock the response of requests.post for a successful API call
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"message": "Success"}

        # Use MessageRequestPayload instead of a plain dictionary
        payload = MessageRequestPayload(
            assistantId=15,
            model="gpt-4o",
            messages=[Message(content="Hello", role="user")]
        )

        response = self.api.send_message(payload)
        self.assertEqual(response, {"message": "Success"})
        mock_post.assert_called_once()

    @patch("FreddyApi.module.requests.post")
    def test_send_message_failure(self, mock_post):
        # Mock the response of requests.post for a failed API call
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {"error": "Bad Request"}

        # Use MessageRequestPayload instead of a plain dictionary
        payload = MessageRequestPayload(
            assistantId=15,
            model="gpt-4o",
            messages=[Message(content="Hello", role="user")]
        )

        with self.assertRaises(Exception) as context:
            self.api.send_message(payload)

        self.assertIn("API request failed", str(context.exception))
        mock_post.assert_called_once()

    @patch("FreddyApi.module.requests.get")
    def test_check_run_status_completed(self, mock_get):
        # Mock the response for a completed run status
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"runStatus": "completed"}

        response = self.api.check_run_status(run_key="dummy_run_key", thread_key="dummy_thread_key")
        self.assertEqual(response, "completed")
        mock_get.assert_called_once()

    @patch("FreddyApi.module.requests.get")
    def test_get_run_response(self, mock_get):
        # Mock the response for getting the final run response
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"text": "Hello! How can I assist you today?"}

        response = self.api.get_run_response(organization_id=0, thread_key="dummy_thread_key")
        self.assertEqual(response["text"], "Hello! How can I assist you today?")
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()