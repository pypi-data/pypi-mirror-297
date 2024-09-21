import json
import unittest
from unittest.mock import patch, Mock
import requests

from pythonlemmy import LemmyHttp
from pythonlemmy.responses import GetFederatedInstancesResponse, GetCommentsResponse, CommentResponse


class TestGetComment(unittest.TestCase):

    @patch('pythonlemmy.lemmyhttp.RequestController')
    def test_get_comment(self, MockRequestController):
        # Arrange
        with open("tests/unit/fixtures/get_comment.json") as f:
            fixture = json.load(f)

        mock_response = Mock(spec=requests.Response)
        mock_response.json.return_value = fixture
        mock_request_controller = MockRequestController.return_value
        mock_request_controller.get_handler.return_value = mock_response

        instance = LemmyHttp("https://lemmy.blahaj.zone")

        # Act
        response = instance.get_comment(20700)

        # Assert
        self.assertEqual(response.json(), fixture)
        response_data = CommentResponse(response)
        self.assertIsNotNone(response_data.comment_view)
        self.assertEqual(2, len(response_data.recipient_ids))
        self.assertEqual(1, response_data.recipient_ids[0])
        self.assertEqual(False, response_data.comment_view.comment.distinguished)


if __name__ == '__main__':
    unittest.main()
