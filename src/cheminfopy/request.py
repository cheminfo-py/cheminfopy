# -*- coding: utf-8 -*-
"""Implementing the basic logic for requests the rest-on-couch API"""
import json
import logging
from typing import Dict, Tuple

import requests

from .errors import AuthenticationError

METHOD_MAP: Dict[str, Tuple] = {
    "GET": (requests.get, {}),
    "POST": (requests.post, {}),
    "DELETE": (requests.delete, {}),
    "PUT": (requests.put, {}),
}

__all__ = ["ELNRequest"]


class ELNRequest:
    """Class that runs the actual request using token authentication."""

    def __init__(self, token: str):
        """

        Args:
            token (str): Token string. Can be any kind of token (user/entry)
                with any rights. If the token does not have suitable rights,
                the library will raise and Exception.
                Tokens can be generated in the ELN using the "Access Token"
                view
        """
        self.token = token
        self.params = {"token": self.token}
        self.logger = logging.getLogger("ELNRequestLogger")
        self.logger.setLevel(logging.DEBUG)
        # Todo: factor out
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _get_header(self, verb: str):
        requests_method, headers = METHOD_MAP[verb.upper()]
        return requests_method, headers

    def _make_request(self, verb: str, url: str, **kwargs) -> requests.Response:
        """Perform the request verb (GET, POST, PUT)"""
        method, headers = self._get_header(verb)
        request = method(url, headers=headers, params=self.params, **kwargs)
        if request.status_code == 401:
            raise AuthenticationError("Request was unauthorized")
        if not request.ok:
            request.raise_for_status()
        return request

    def post(self):
        """Make a POST request."""
        raise NotImplementedError("POST requests are currently not supported")

    def delete(self, url: str) -> requests.Response:
        response = self._make_request("DELETE", url)
        return response

    def put(self, url: str, data: object = None, json_payload: dict = None) -> requests.Response:
        """Make a PUT request to the URL with the provided data

        Args:
            url (str): URL to which the request should be made
            data (object): Some data to be sent with the request. Defaults to None
            json_payload (dict): JSON payload. If not None, this method will default to
                using the JSON payload instead of the data
        Returns:
            [requests.Response]: Response of the request
        """
        if json_payload is not None:
            response = self._make_request("PUT", url, json=json_payload)
        else:
            response = self._make_request("PUT", url, data=data)
        return response

    def get(self, url: str) -> requests.Response:
        """Make a GET request to the URL

        Args:
            url (str): URL to which the request should be made

        Returns:
            requests.Response: Response of the request
        """
        response = self._make_request("GET", url)
        if response.status_code == 401:
            raise AuthenticationError("Request was unauthorized")
        return json.loads(response.text)

    def get_file(self, url: str) -> requests.Response:
        """Alias for GET request"""
        response = self._make_request("GET", url)
        return response
