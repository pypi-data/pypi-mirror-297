import logging
from collections.abc import Callable
from typing import Optional

import requests

from .types import UploadFile


class RequestController:
    _session: requests.Session
    _headers: Optional[dict]

    def __init__(self, headers: Optional[dict] = None):
        self._headers = headers
        self.create_session(None)
        self.logger = logging.getLogger(__name__)

    def create_session(self, jwt: Optional[str]):
        """ create_session: create a `requests.Session` session given supplied
        headers and jwt/authentication key

        Args:
            headers (dict): session headers
            jwt (str): jwt/authentication key

        Returns:
            requests.Session: open session
        """

        session = requests.Session()
        if self._headers is not None:
            session.headers.update(self._headers)
        if jwt is not None:
            session.cookies.set("jwt", jwt)

        self._session = session

    def post_handler(self, url: str, json: dict, params: dict = None) -> requests.Response:
        """ post_handler: handles all POST operations for Plemmy

        Args:
            url (str): URL of API call
            json (dict): json/form data
            params (dict, optional): parameters for POST operation

        Returns:
            requests.Response: server response for POST operation
        """

        return self._run_request(lambda: self._session.post(url, json=json, params=params))

    def file_handler(self, url: str, files: UploadFile) -> requests.Response:
        """ file_handler: handles all POST operations for Plemmy

        Args:
            url (str): URL of API call
            files: files to be uploaded

        Returns:
            requests.Response: server response for POST operation
        """

        return self._run_request(lambda: self._session.post(url, files=files, timeout=60))

    def put_handler(self, url: str, json: dict, params: dict = None) -> requests.Response:
        """ put_handler: handles all PUT operations for Plemmy

        Args:
            session (requests.Session): open Lemmy session
            url (str): URL of API call
            json (dict): json/form data
            params (dict, optional): parameters for PUT operation

        Returns:
            requests.Response: server response for PUT operation
        """

        return self._run_request(lambda: self._session.put(url, json=json, params=params))

    def get_handler(self, url: str, json: Optional[dict] = None, params: dict = None) -> requests.Response:
        """ get_handler: handles all GET operations for Plemmy

        Args:
            session (requests.Session): open Lemmy session
            url (str): URL of API call
            json (dict): json/form data (optional)
            params (dict, optional): parameters for GET operation

        Returns:
            requests.Response: server response for GET operation
        """

        return self._run_request(lambda: self._session.get(url, json=json, params=params))

    def _run_request(self, call: Callable[[], requests.Response]) -> Optional[requests.Response]:
        try:
            re = call()
            self.logger.debug(f"Code: {re.status_code}")
            if re.status_code >= 300:
                self.logger.error(f"Error response: {re.text}")
        except requests.exceptions.RequestException as ex:
            self.logger.error(f"GET error: {ex}")
            return None
        return re