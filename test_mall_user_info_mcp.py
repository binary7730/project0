import unittest
from unittest.mock import patch, Mock
import json # For json.JSONDecodeError
import requests # For requests.exceptions

# Assuming mall_user_info_mcp.py is in the same directory or accessible in PYTHONPATH
from mall_user_info_mcp import get_user_info, UserInfoError

class TestGetUserInfo(unittest.TestCase):

    @patch('mall_user_info_mcp.requests.get')
    def test_successful_api_call(self, mock_get):
        """Test a successful API call with valid JSON response."""
        sample_mall_id = "test_success"
        expected_data = {"userId": sample_mall_id, "name": "Test User"}

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_data
        mock_response.text = json.dumps(expected_data) # For error messages if json decoding fails elsewhere
        mock_get.return_value = mock_response

        result = get_user_info(sample_mall_id)
        self.assertEqual(result, expected_data)
        mock_get.assert_called_once_with(
            f"https://infra-apigw.hanpda.com/ptool_userinfo/user_info.php?display_type=json&user_id={sample_mall_id}",
            timeout=10
        )

    @patch('mall_user_info_mcp.requests.get')
    def test_api_error_status_code_404(self, mock_get):
        """Test API returning a 404 error status code."""
        sample_mall_id = "test_404"

        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(UserInfoError, f"API request failed with status code 404: Not Found"):
            get_user_info(sample_mall_id)
        mock_get.assert_called_once_with(
            f"https://infra-apigw.hanpda.com/ptool_userinfo/user_info.php?display_type=json&user_id={sample_mall_id}",
            timeout=10
        )

    @patch('mall_user_info_mcp.requests.get')
    def test_api_error_status_code_500(self, mock_get):
        """Test API returning a 500 error status code."""
        sample_mall_id = "test_500"

        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(UserInfoError, f"API request failed with status code 500: Internal Server Error"):
            get_user_info(sample_mall_id)

    @patch('mall_user_info_mcp.requests.get')
    def test_network_error_timeout(self, mock_get):
        """Test a network error like a timeout."""
        sample_mall_id = "test_timeout"
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

        with self.assertRaisesRegex(UserInfoError, f"API request timed out for mallid: {sample_mall_id}"):
            get_user_info(sample_mall_id)
        mock_get.assert_called_once_with(
            f"https://infra-apigw.hanpda.com/ptool_userinfo/user_info.php?display_type=json&user_id={sample_mall_id}",
            timeout=10
        )

    @patch('mall_user_info_mcp.requests.get')
    def test_network_error_connection(self, mock_get):
        """Test a generic network connection error."""
        sample_mall_id = "test_connect_error"
        mock_get.side_effect = requests.exceptions.ConnectionError("Failed to connect")

        with self.assertRaisesRegex(UserInfoError, f"API request failed for mallid {sample_mall_id}: Failed to connect"):
            get_user_info(sample_mall_id)

    @patch('mall_user_info_mcp.requests.get')
    def test_invalid_json_response(self, mock_get):
        """Test handling of an invalid JSON response."""
        sample_mall_id = "test_invalid_json"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "This is not JSON"
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "This is not JSON", 0)
        mock_get.return_value = mock_response

        # Check that the error message contains part of the invalid response text
        with self.assertRaisesRegex(UserInfoError, f"Failed to decode JSON response for mallid {sample_mall_id}.*Response text: This is not JSON..."):
            get_user_info(sample_mall_id)
        mock_get.assert_called_once_with(
            f"https://infra-apigw.hanpda.com/ptool_userinfo/user_info.php?display_type=json&user_id={sample_mall_id}",
            timeout=10
        )

if __name__ == "__main__":
    unittest.main()
