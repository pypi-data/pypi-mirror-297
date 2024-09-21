import unittest
import os
import json
from unittest import mock
from unittest.mock import mock_open, patch
from pydantic import BaseModel
from greeng3_python.k8s.secrets import SecretsJSON


# Define a mock Pydantic model for testing
class MockSecretsModel(BaseModel):
    username: str
    password: str


class TestSecretsJSON(unittest.TestCase):

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"username": "admin", "password": "secret"}')
    def test_valid_json_creates_model(self, mock_file, mock_exists):
        # Create SecretsJSON with valid data
        secrets = SecretsJSON('/fake/path/to/secrets.json', MockSecretsModel)
        
        # Ensure the model was created successfully
        self.assertIsNotNone(secrets.model)
        self.assertEqual(secrets.model.username, "admin")
        self.assertEqual(secrets.model.password, "secret")

    @patch('os.path.exists', return_value=False)
    @patch('logging.error')
    def test_file_does_not_exist(self, mock_log_error, mock_exists):
        # Try to create SecretsJSON when the file does not exist
        secrets = SecretsJSON('/fake/path/to/secrets.json', MockSecretsModel)
        
        # Ensure that model is None and correct log message is recorded
        self.assertIsNone(secrets.model)
        mock_log_error.assert_called_with("Secrets file '/fake/path/to/secrets.json' does not exist.")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open)
    @patch('logging.error')
    def test_io_error_when_reading_file(self, mock_log_error, mock_file, mock_exists):
        # Simulate an IOError when opening the file
        mock_file.side_effect = IOError("IO Error")
        
        secrets = SecretsJSON('/fake/path/to/secrets.json', MockSecretsModel)
        
        # Ensure model is None and the IOError is logged
        self.assertIsNone(secrets.model)
        mock_log_error.assert_called_with("Error reading secrets file '/fake/path/to/secrets.json': IO Error")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('logging.error')
    def test_json_decode_error(self, mock_log_error, mock_file, mock_exists):
        # Simulate invalid JSON
        secrets = SecretsJSON('/fake/path/to/secrets.json', MockSecretsModel)
        
        # Ensure model is None and JSONDecodeError is logged
        self.assertIsNone(secrets.model)
        mock_log_error.assert_called_with("Error parsing JSON: Expecting value: line 1 column 1 (char 0)")

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', new_callable=mock_open, read_data='{"username": "admin"}')  # Missing password
    @patch('logging.error')
    def test_invalid_model_creation(self, mock_log_error, mock_file, mock_exists):
        # Simulate JSON that fails to create the Pydantic model (missing password)
        secrets = SecretsJSON('/fake/path/to/secrets.json', MockSecretsModel)
        
        # Ensure model is None and that the error when creating the model is logged
        self.assertIsNone(secrets.model)
        self.assertTrue(mock_log_error.called)
        self.assertIn("Error creating model", mock_log_error.call_args[0][0])


if __name__ == '__main__':
    unittest.main()
