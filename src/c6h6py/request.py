# -*- coding: utf-8 -*-
import json
import logging
from typing import Dict, Tuple
from urllib.parse import urljoin

import requests

METHOD_MAP: Dict[str, Tuple] = {
    "GET": (requests.get, {}),
    "POST": (requests.post, {}),
    "DELETE": (requests.delete, {}),
    "PUT": (requests.put, {}),
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

    def _make_request(self, verb: str, url: str, **kwargs):
        method, headers = self._get_header(verb)
        request = method(url, headers=headers, params=self.params, **kwargs)
        if not request.ok:
            request.raise_for_status()
        return request

    def post(self):
        ...

    def post_file(self, url: str, data: str):
        response = self._make_request("POST", url, data=data)
        return response

    def get(self, url: str):
        response = self._make_request("GET", url)
        return json.loads(response.text)

    def get_file(self, url: str):
        response = self._make_request("GET", url)
        return response
