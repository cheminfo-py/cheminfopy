# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from .manager import Manager

__all__ = ["Sample"]


class Sample(Manager):
    """Sample manager handles operations on samples"""

    def __init__(self, *args, **kwargs):
        self.sample_uuid = kwargs.pop("sample_uuid", None)
        super().__init__(*args, **kwargs)
        self._sample_toc = None

    def put_attachment(self, attachment_type: str, name: str, filecontent):
        query_path = f"entry/{self.sample_uuid}/spectra/{attachment_type}/{name}"
        url = urljoin(self.instance, query_path)
        self.requester.put(url, data=filecontent)

    def get_attachment(self, attachment_type: str, name: str):
        query_path = f"entry/{self.sample_uuid}/spectra/{attachment_type}/{name}"
        url = urljoin(self.instance, query_path)
        return self.requester.get_file(url).text

    @property
    def has_right(self, right: str):
        query_path = f"entry/{self.sample_uuid}/_rights/{right}"
        url = urljoin(self.instance, query_path)
        return self.requester.get(url).text

    @property
    def toc(self):
        return self._get_toc()

    @property
    def molfile(self):
        toc = self.toc
        return toc["$content"]["general"]["molfile"]

    @property
    def mw(self):
        toc = self.toc
        return toc["$content"]["general"]["mw"]

    @property
    def em(self):
        toc = self.toc
        return toc["$content"]["general"]["em"]

    @property
    def id(self):
        toc = self.toc
        return toc["$content"]["_id"]

    @property
    def mf(self):
        toc = self.toc
        return toc["$content"]["general"]["mf"]

    @property
    def spectra(self):
        toc = self.toc
        return toc["$content"]["spectra"]

    @property
    def owners(self):
        toc = self.toc
        return toc["$owners"]

    def _get_toc(self):

        query_path = f"entry/{self.sample_uuid}"
        url = urljoin(self.instance, query_path)
        self._sample_toc = self.requester.get(url)

        return self._sample_toc

    def _update_toc(self, new_toc):
        query_path = f"entry/{self.sample_uuid}"
        url = urljoin(self.instance, query_path)
        print(url)
        self._sample_toc = self.requester.put(url, data=new_toc)
