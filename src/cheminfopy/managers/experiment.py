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
    def kind(self):
        """Kind of the entry"""
        return self.toc["$kind"]

    @property
    def title(self):
        """Title of the reaction"""
        return self.toc["$content"]["title"]

    @property
    def products(self):
        """Products of the reaction"""
        return self.toc["$content"]["products"]

    @property
    def reagents(self):
        """Reagents of the reaction"""
        return self.toc["$content"]["reagents"]

    @property
    def procedure(self):
        """Procedure of the reaction"""
        return self.toc["$content"]["procedure"]

    @property
    def reactionRXN(self):
        """Reaction RXN file"""
        return self.toc["$content"]["reactionRXN"]  

    @property
    def remarks(self):
        """Remarks of the reaction"""
        return self.toc["$content"]["remarks"]

    @property
    def date(self):
        """Date of the experiment"""
        return self.toc["$content"]["date"]

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
