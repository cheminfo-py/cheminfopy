# -*- coding: utf-8 -*-
from ..request import ELNRequest

__all__ = ["Manager"]


def _sanitize_instance(instance):
    if instance[-1] != "/":
        instance += "/"
    return instance


class Manager:
    """Base class for all managers"""

    def __init__(self, instance: str, token: str, **kwargs):
        """A manager instance provides the basic functionality
        to interact with the rest-on-couch API

        Args:
            instance (str): URL the the ELN instance, for example
                https://mydb.cheminfo.org/db/eln for the c6h6.org
                deployment

            token (str): Token string. Can be any kind of token (user/entry)
                with any rights. If the token does not have suitable rights,
                the library will raise and Exception.
                Tokens can be generated in the ELN using the "Access Token"
                view
        """
        self.instance = _sanitize_instance(instance)
        self.token = token
        self.requester = ELNRequest(self.token)
