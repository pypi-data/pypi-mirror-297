import json
import unittest
from unittest.mock import patch, Mock

import pytest
import requests

from pythonlemmy import LemmyHttp
from pythonlemmy.responses import GetFederatedInstancesResponse, LoginResponse


class TestSetJWT(unittest.TestCase):

    def test_set_jwt(self):
        # Arrange
        instance = LemmyHttp("https://lemmy.blahaj.zone")

        # Act
        instance.set_jwt("test")

        # Assert
        self.assertEqual("test", instance._request_controller._session.cookies.get("jwt"))


if __name__ == '__main__':
    unittest.main()
