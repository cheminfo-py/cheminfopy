# -*- coding: utf-8 -*-
"""Dealing with experiments/reactions"""
from urllib.parse import urljoin

from .manager import Manager

__all__ = ["Experiment"]


class Experiment(Manager):
    """Experiment manager handles operations on experiments"""

    def __init__(self, *args, **kwargs):
        """

        Args:
            instance (str): URL the the ELN instance, for example
                https://mydb.cheminfo.org/db/eln for the c6h6.org
                deployment

            token (str): Token string. Can be any kind of token (user/entry)
                with any rights. If the token does not have suitable rights,
                the library will raise and Exception.
                Tokens can be generated in the ELN using the "Access Token"
                view

            experiment_uuid (str): UUID of the experiment
        """
        self.experiment_uuid = kwargs.pop("experiment_uuid", None)
        super().__init__(*args, **kwargs)
        self._experiment_toc = None

    @property
    def id(self):  # pylint: disable=invalid-name
        """UUID of the reaction"""
        return self.toc["_id"]

    @property
    def revision(self):
        """Revision of the reaction"""
        return self.toc["_rev"]

    @property
    def owners(self):
        """Owners of the reaction"""
        return self.toc["$owners"]

    def _get_toc(self):
        """Make GET request for the table of contents"""
        query_path = f"entry/{self.experiment_uuid}"
        url = urljoin(self.instance, query_path)
        self._experiment_toc = self.requester.get(url)

        return self._experiment_toc

    @property
    def toc(self):
        """Get the table of contents entry for this experiment"""
        return self._get_toc()
