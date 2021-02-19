from urllib.parse import urljoin
from typing import Dict, Tuple
import requests
import logging
import json

METHOD_MAP: Dict[str, Tuple] = {
    "GET": (requests.get, {}),
    "POST": (requests.post, {}),
    "DELETE": (requests.delete, {}),
}


class ELNRequest:
    def __init__(self, token):
        self.token = token
        self.params = {"token": self.token}
        self.logger = logging.getLogger("ELNRequestLogger")
        self.logger.setLevel(logging.DEBUG)
        # Todo: factor out
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def _get_header(self, verb: str):
        requests_method, headers = METHOD_MAP[verb.upper()]
        return requests_method, headers

    def _make_request(self, verb: str, url: str):
        method, headers = self._get_header(verb)
        request = method(url, headers=headers, params=self.params)
        if not request.ok:
            request.raise_for_status()
        return request

    def post(self):
        ...

    def put(self):
        ...

    def get(self, url: str):
        response = self._make_request("GET", url)
        return json.loads(response.text)
