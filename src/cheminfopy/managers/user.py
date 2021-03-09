# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from .manager import Manager

__all__ = ["User"]


class User(Manager):
    """User manager handles operations on users"""

    def get_sample_toc(self):
        """Returns the raw table of all samples the user has access to"""
        query_path = "_query/sample_toc"
        url = urljoin(self.instance, query_path)
        return self.requester.get(url)
