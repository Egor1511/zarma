import json
import os
import unittest
from unittest.mock import patch, MagicMock

from test_tasks.first_task.first_task import APIClient


class TestAPIClient(unittest.TestCase):
    def setUp(self) -> None:
        self.api_client = APIClient('https://jsonplaceholder.typicode.com')
        self.sample_data = [
            {"userId": 1, "id": 1, "title": "test title", "body": "test body"}]
        self.test_filename = 'test_posts.json'

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.sample_data
        mock_get.return_value = mock_response

        data = self.api_client.fetch_data('posts')
        self.assertEqual(data, self.sample_data)
        mock_get.assert_called_once_with(
            'https://jsonplaceholder.typicode.com/posts')

    @patch('requests.get')
    def test_fetch_data_failure(self, mock_get: MagicMock) -> None:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.api_client.fetch_data('posts')
        self.assertIn('Failed to connect to API', str(context.exception))
        mock_get.assert_called_once_with(
            'https://jsonplaceholder.typicode.com/posts')

    def test_save_to_file(self) -> None:
        self.api_client.save_to_file(self.sample_data, self.test_filename)

        self.assertTrue(os.path.exists(self.test_filename))

        with open(self.test_filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self.assertEqual(data, self.sample_data)

        os.remove(self.test_filename)


if __name__ == "__main__":
    unittest.main()
