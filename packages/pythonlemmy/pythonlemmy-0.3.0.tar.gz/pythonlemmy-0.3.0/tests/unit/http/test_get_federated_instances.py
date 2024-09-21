import json
import unittest
from unittest.mock import patch, Mock
import requests

from pythonlemmy import LemmyHttp
from pythonlemmy.responses import GetFederatedInstancesResponse


class TestGetFederatedInstances(unittest.TestCase):

    @staticmethod
    def exception_side_effect():
        raise ValueError("Invalid JSON")

    @patch('pythonlemmy.lemmyhttp.RequestController')
    def test_get_federated_instances_success(self, MockRequestController):
        # Arrange
        with open("tests/unit/fixtures/get_federated_instances.json") as f:
            fixture = json.load(f)

        mock_response = Mock(spec=requests.Response)
        mock_response.json.return_value = fixture
        mock_request_controller = MockRequestController.return_value
        mock_request_controller.get_handler.return_value = mock_response

        instance = LemmyHttp("https://lemmy.blahaj.zone")

        # Act
        response = instance.get_federated_instances()

        # Assert
        self.assertEqual(response.json(), fixture)
        response_data = GetFederatedInstancesResponse(response)
        self.assertIsNotNone(response_data.federated_instances)
        self.assertEqual(2, len(response_data.federated_instances.linked))
        self.assertEqual(3, response_data.federated_instances.linked[0].id)

    @patch('pythonlemmy.lemmyhttp.RequestController')
    def test_get_federated_instances_no_federated_instances(self, MockRequestController):
        # Arrange
        with open("tests/unit/fixtures/get_federated_instances_none.json") as f:
            fixture = json.load(f)

        mock_response = Mock(spec=requests.Response)
        mock_response.json.return_value = fixture
        mock_request_controller = MockRequestController.return_value
        mock_request_controller.get_handler.return_value = mock_response

        instance = LemmyHttp("https://lemmy.blahaj.zone")

        # Act
        response = instance.get_federated_instances()

        # Assert
        response_data = GetFederatedInstancesResponse(response)
        self.assertIsNotNone(response_data.federated_instances)
        self.assertEqual(0, len(response_data.federated_instances.linked))

if __name__ == '__main__':
    unittest.main()
