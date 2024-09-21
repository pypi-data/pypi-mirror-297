import json
import unittest
from unittest.mock import patch, Mock

import pytest
import requests

from pythonlemmy import LemmyHttp
from pythonlemmy.responses import GetFederatedInstancesResponse, LoginResponse


class TestLogin(unittest.TestCase):

    @staticmethod
    def exception_side_effect():
        raise ValueError("Invalid JSON")

    @patch('pythonlemmy.lemmyhttp.RequestController')
    def test_login_success(self, MockRequestController):
        # Arrange
        with open("tests/unit/fixtures/post_login.json") as f:
            fixture = json.load(f)

        mock_response = Mock(spec=requests.Response)
        mock_response.json.return_value = fixture
        mock_response.status_code = 200

        mock_request_controller = MockRequestController.return_value
        mock_request_controller.post_handler.return_value = mock_response

        instance = LemmyHttp("https://lemmy.blahaj.zone")

        # Act
        response = instance.login("test", "password")

        # Assert
        mock_request_controller.post_handler.assert_called_with(
            'https://lemmy.blahaj.zone/api/v3/user/login',
            json={'username_or_email': 'test', 'password': 'password'},
            params=None
        )
        self.assertEqual(response.json(), fixture)
        response_data = LoginResponse(response)
        self.assertIsNotNone(response_data.jwt is not None)
        mock_request_controller.create_session.assert_called_with("jwt")

    @patch('pythonlemmy.lemmyhttp.RequestController')
    def test_login_failure(self, MockRequestController):
        # Arrange
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 400

        mock_request_controller = MockRequestController.return_value
        mock_request_controller.post_handler.return_value = mock_response

        instance = LemmyHttp("https://lemmy.blahaj.zone")

        # Act
        with pytest.raises(Exception):
            response = instance.login("test", "password")

        # Assert
        mock_request_controller.post_handler.assert_called_with(
            'https://lemmy.blahaj.zone/api/v3/user/login',
            json={'username_or_email': 'test', 'password': 'password'},
            params=None
        )
        self.assertFalse(mock_request_controller.create_session.called)


if __name__ == '__main__':
    unittest.main()
