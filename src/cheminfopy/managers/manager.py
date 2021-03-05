# -*- coding: utf-8 -*-
from typing import Union

from ..request import ELNRequest

__all__ = ["Manager"]


class Manager:
    """Base class for all managers"""

    def __init__(self, instance: str, token: str, **kwargs):
        self.instance = instance
        self.token = token
        self.requester = ELNRequest(self.token)
