from io import TextIOWrapper
from typing import Optional, Union

from requests import Response

File = tuple[Optional[str], Union[bytes, str, TextIOWrapper]]
UploadFile = dict[str, File]


class ResponseWrapper(object):
    def __init__(self, data: Response):
        self.parse(data.json())

    def parse(self, data: dict):
        pass
