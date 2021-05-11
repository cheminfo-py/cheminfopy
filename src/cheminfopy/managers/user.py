# -*- coding: utf-8 -*-
"""Handle operations on the user level"""
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

    def get_sample(self, uuid: str):
        """Get a sample object for a sample UUID"""
        return Sample(instance=self.instance, token=self.token, sample_uuid=uuid)

    def get_experiment(self, uuid: str):
        """Get a experiment object for an experiment UUID"""
        return Experiment(
            instance=self.instance, token=self.token, experiment_uuid=uuid
        )
