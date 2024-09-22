import unittest
from unittest.mock import patch, MagicMock
import requests
import json

from how2validate.utility.config_utility import get_active_secret_status, get_inactive_secret_status
from how2validate.validators.npm.npm_access_token import validate_npm_access_token



# Import the function you want to test

class TestValidateNpmAccessToken(unittest.TestCase):

    @patch('requests.get')
    def test_valid_token_success(self, mock_get):
        """
        Test the case where the NPM access token is valid and the API returns 200 with a valid JSON response.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"user": "valid_user"}
        mock_get.return_value = mock_response

        service = "npm"
        secret = "valid_secret"
        response = True
        report = False

        result = validate_npm_access_token(service, secret, response, report)

        # Validate that we get the correct response and status
        self.assertIn(get_active_secret_status(), result)
        self.assertIn('"user": "valid_user"', result)

    @patch('requests.get')
    def test_inactive_token(self, mock_get):
        """
        Test the case where the NPM access token is invalid, and the API returns a 401 status code.
        """
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_get.return_value = mock_response

        service = "npm"
        secret = "invalid_secret"
        response = True
        report = False

        result = validate_npm_access_token(service, secret, response, report)

        # Validate that we get the correct response and status
        self.assertIn(get_inactive_secret_status(), result)
        self.assertIn("Unauthorized", result)

    @patch('requests.get')
    def test_json_decode_error(self, mock_get):
        """
        Test the case where the NPM API returns a 200 response but the body is not valid JSON.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "Not a JSON response"
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "document", 0)
        mock_get.return_value = mock_response

        service = "npm"
        secret = "valid_secret"
        response = True
        report = False

        result = validate_npm_access_token(service, secret, response, report)

        # Validate that the function correctly reports a JSONDecodeError
        self.assertIn(get_active_secret_status(), result)
        self.assertIn("Response is not a valid JSON", result)

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        """
        Test the case where a connection error occurs during the request.
        """
        mock_get.side_effect = requests.ConnectionError("Failed to establish a connection")

        service = "npm"
        secret = "valid_secret"
        response = True
        report = False

        result = validate_npm_access_token(service, secret, response, report)

        # Validate that the function handles connection errors
        self.assertIn(get_inactive_secret_status(), result)
        self.assertIn("Failed to establish a connection", result)

    @patch('npm_access_token.requests.get')
    def test_timeout_error(self, mock_get):
        """
        Test the case where a timeout occurs during the request.
        """
        mock_get.side_effect = requests.Timeout("Request timed out")

        service = "npm"
        secret = "valid_secret"
        response = True
        report = False

        result = validate_npm_access_token(service, secret, response, report)

        # Validate that the function handles timeouts
        self.assertIn(get_inactive_secret_status(), result)
        self.assertIn("Request timed out", result)

    @patch('requests.get')
    def test_empty_response(self, mock_get):
        """
        Test the case where the API returns a 200 response with an empty body.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = ""  # Empty response body
        mock_get.return_value = mock_response

        service = "npm"
        secret = "valid_secret"
        response = True
        report = False

        result = validate_npm_access_token(service, secret, response, report)

        # Validate that the function handles empty responses
        self.assertIn(get_active_secret_status(), result)
        self.assertIn("{}", result)  # Empty JSON string

if __name__ == '__main__':
    unittest.main()
