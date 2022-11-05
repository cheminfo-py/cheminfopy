# -*- coding: utf-8 -*-
"""Handle operations on the user level"""
from typing import Collection
from urllib.parse import urljoin

from .experiment import Experiment
from .manager import Manager
from .sample import Sample

__all__ = ["User"]


class User(Manager):
    """User manager handles operations on users"""

    def get_sample_toc(self):
        """Returns the raw table of all samples the user has access to"""
        query_path = "_query/sample_toc"
        url = urljoin(self.instance, query_path)
        return self.requester.get(url)

    def get_experiment_toc(self):
        """Returns the raw table of all experiments the user has access to"""
        query_path = "_query/reactionToc"
        url = urljoin(self.instance, query_path)
        return self.requester.get(url)

    def get_sample(self, uuid: str):
        """Get a sample object for a sample UUID"""
        return Sample(instance=self._instance, token=self.token, sample_uuid=uuid)

    def get_experiment(self, uuid: str):
        """Get a experiment object for an experiment UUID"""
        return Experiment(instance=self.instance, token=self.token, experiment_uuid=uuid)

    @property
    def is_valid_token(self):
        """Checks if the token is actually a user token"""
        url = urljoin(self.instance, f"token/{self.token}")
        try:
            response = self.requester.get(url)
            is_user_token = response["$kind"] == "user"
            return is_user_token
        except Exception:  # pylint:disable=broad-except
            return False

    def has_rights(self, rights: Collection[str]) -> bool:
        """Checks if the token with which the manager was initialized
        has certain rights.

        Args:
            rights (Collection[str]): right to test ("write", "create", "read",
                "addAttachment" are the most relevant ones)

        Returns:
            [bool]: True if the manager instance has the rights
        """
        query_path = f"token/{self.token}"
        url = urljoin(self.instance, query_path)

        try:
            response = self.requester.get(url)
            rights_in_token = response["rights"]
            for right in rights:
                if not right in rights_in_token:
                    return False
            return True
        except Exception:  # pylint:disable=broad-except
            return False
