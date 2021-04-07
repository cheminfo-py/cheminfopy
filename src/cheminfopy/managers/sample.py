# -*- coding: utf-8 -*-
from typing import Union
from urllib.parse import urljoin

from ..constants import VALID_SPECTRUM_TYPES
from ..errors import InvalidAttachmentTypeError
from .manager import Manager
from .utils import _new_toc

__all__ = ["Sample"]


class Sample(Manager):
    """Sample manager handles operations on samples"""

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

            sample_uuid (str): UUID of the sample
        """
        self.sample_uuid = kwargs.pop("sample_uuid", None)
        super().__init__(*args, **kwargs)
        self._sample_toc = None

    def put_spectrum(
        self,
        spectrum_type: str,
        name: str,
        filecontent: str,
        metadata: dict = None,
        source_info: Union[dict, None] = None,
    ):
        """This methods allows to add spectra to a sample.
        Follow the dataschema at https://cheminfo.github.io/data_schema/.
        In particular, use JCAMP-DX files for spectra. You can use the pytojcamp library
        (https://github.com/cheminfo-py/pytojcamp) to convert Python dictionaries to JCAMP-DX
        files.

        Args:
            spectrum_type (str): spectrum type. Valid types are in VALID_SPECTRUM_TYPES
            name (str): filename (with extension)
            filecontent (str): String with the content of the file
            metadata (str): Metadata dictionary. Please follow the schema at
                https://cheminfo.github.io/data_schema/.
                For example, for gas adsorption isotherms you might want
                to add the keys 'gas' and 'temperature'.
                Defaults to None.
            source_info (Union[dict, None], optional): You can provide a dictionary with source information.
                Allowed keys are "name", "url", 'uuid", "doi". Use this to describe the source of the data
                you want to attach to the sample.
                If you do not provide this dictionary / leave the default value of None,
                we will default the values in DEFAULT_SOURCE_DICT.
                Defaults to None.

        Raises:
            InvalidAttachmentTypeError: If the selected type is not supported by the schema of the ELN.
                The allowed types are in VALID_SPECTRUM_TYPES
        """
        if spectrum_type not in VALID_SPECTRUM_TYPES:
            raise InvalidAttachmentTypeError(
                f"Invalid spectrum type {spectrum_type}. Allowed spectrum types are {', '.join(VALID_SPECTRUM_TYPES)}."
            )
        query_path = f"entry/{self.sample_uuid}/spectra/{spectrum_type}/{name}"
        url = urljoin(self.instance, query_path)
        self.requester.put(url, data=filecontent)
        new_toc = _new_toc(self.toc, spectrum_type, name, metadata, source_info)
        self._update_toc(new_toc)

    def get_spectrum(self, spectrum_type: str, name: str):
        """Allows to get a specific spectrum from the ELN.
        For this you need to select the type and the filename of the spectrum.
        You can get an overview of all the attached spectra from the table of contents of the sample.

        Args:
            spectrum_type (str): spectrum type. Valid types are in VALID_SPECTRUM_TYPES
            name (str): filename (with extension)

        Returns:
            [str]: The filecontent of the selected spectrum.

        Raises:
            InvalidAttachmentTypeError: If the selected type is not supported by the schema of the ELN.
                The allowed types are in VALID_SPECTRUM_TYPES
        """
        if spectrum_type not in VALID_SPECTRUM_TYPES:
            raise InvalidAttachmentTypeError(
                f"Invalid spectrum type {spectrum_type}. Allowed spectrum types are {', '.join(VALID_SPECTRUM_TYPES)}."
            )
        query_path = f"entry/{self.sample_uuid}/spectra/{spectrum_type}/{name}"
        url = urljoin(self.instance, query_path)
        return self.requester.get_file(url).text

    @property
    def has_right(self, right: str) -> bool:
        """Checks if the token with which the manager was initialized
        has certain rights.

        Args:
            right (str): right to test ("write", "create", "read",
                "addAttachment" are the most relevant ones)

        Returns:
            [bool]: True if the manager instance has the rights
        """
        query_path = f"entry/{self.sample_uuid}/_rights/{right}"
        url = urljoin(self.instance, query_path)
        resp = self.requester.get(url).text
        if resp == "true":
            return True
        return False

    @property
    def id(self):
        """UUID of the sample"""
        return self.toc["_id"]

    @property
    def revision(self):
        """Revision of the document"""
        return self.toc["_rev"]

    @property
    def owners(self):
        """Owners of the sample"""
        return self.toc["$owners"]

    @property
    def type(self):
        """Type of the document"""
        return self.toc["$entry"]

    @property
    def last_modified_by(self):
        """Returns the username who performed the last modification"""
        return self.toc["$lastModification"]

    @property
    def modification_date(self):
        """Returns the date of the last modification"""
        return self.toc["$modificationDate"]

    @property
    def creation_date(self):
        """Returns the creation date"""
        return self.toc["$creationDate"]

    @property
    def toc(self):
        """Get the table of contents entry for this sample"""
        return self._get_toc()

    @property
    def molfile(self):
        """Return the molfile for this sample"""
        toc = self.toc
        return toc["$content"]["general"]["molfile"]

    @property
    def mw(self):
        """Return the molecular weight in g/mol"""
        toc = self.toc
        return toc["$content"]["general"]["mw"]

    @property
    def em(self):
        """Returns the exact mass in Dalton"""
        toc = self.toc
        return toc["$content"]["general"]["em"]

    @property
    def mf(self):
        """Returns a string with the molecular formula"""
        toc = self.toc
        return toc["$content"]["general"]["mf"]

    @property
    def spectra(self):
        """Lists all spectra that are attached to the sample"""
        toc = self.toc
        return toc["$content"]["spectra"]

    def _get_toc(self):
        """Make GET request for the table of contents"""
        query_path = f"entry/{self.sample_uuid}"
        url = urljoin(self.instance, query_path)
        self._sample_toc = self.requester.get(url)

        return self._sample_toc

    def _update_toc(self, new_toc: dict):
        """Make a PUT request to update the table of contents"""
        query_path = f"entry/{self.sample_uuid}"
        url = urljoin(self.instance, query_path)
        self.requester.put(url, json=new_toc)
