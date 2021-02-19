from typing import Union
from .request import ELNRequest
from urllib.parse import urljoin


class Manager:
    """Base class for all managers"""

    def __init__(self, instance: str, token: str, **kwargs):
        self.instance = instance
        self.token = token
        self.requester = ELNRequest(self.token)


class SampleManager(Manager):
    """Sample manager handles operations on samples"""

    def __init__(self, *args, **kwargs):
        self.sample_uuid = kwargs.pop("sample_uuid", None)
        super().__init__(*args, **kwargs)

    def put_spectrum(self, spectrum_type: str, jcamp):
        ...

    def get_spectrum(self, spectrum_type: str, name):
        ...

    def get_sample_toc(self):
        query_path = f"entry/{self.sample_uuid}"
        url = urljoin(self.instance, query_path)
        return self.requester.get(url)


class ExperimentManager(Manager):
    """Experiment manager handles operations on experiments"""


class UserManager(Manager):
    """User manager handles operations on users"""

    def get_toc(self):
        query_path = "_query/sample_toc"
        url = urljoin(self.instance, query_path)
        return self.requester.get(url)
