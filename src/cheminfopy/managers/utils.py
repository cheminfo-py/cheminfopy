# -*- coding: utf-8 -*-
"""Helper functions for the manager classes"""

from copy import deepcopy
from pathlib import Path
from urllib.parse import urljoin

import requests

from ..constants import DEFAULT_SOURCE_DICT
from ..errors import InvalidInstanceUrlError, InvalidSourceError


def _new_toc(toc, dtype, filename, metadata=None, source_dict=None):
    """Create an updated TOC string"""
    toc_copy = deepcopy(toc)
    if source_dict is None:
        source_dict = DEFAULT_SOURCE_DICT
    else:
        for key, value in source_dict.items():
            if key not in DEFAULT_SOURCE_DICT.keys():
                raise InvalidSourceError(
                    f"Invalid source key {key}.\
                         Allowed source keys ares {DEFAULT_SOURCE_DICT.keys()}"
                )
            if not isinstance(value, str):
                raise InvalidSourceError("Source values must be strings")

    extension = Path(filename).suffix.replace(".", "")
    append_dict = {
        "source": source_dict,
        extension: {"filename": f"spectra/{dtype}/{filename}"},
    }
    if isinstance(metadata, dict):
        for key, value in metadata.items():
            append_dict[key] = value

    try:
        toc_copy["$content"]["spectra"][type].append(append_dict)
    except KeyError:
        # first entry
        toc_copy["$content"]["spectra"][type] = [append_dict]
    return toc_copy


def sanitize_instance_url(url: str) -> str:
    """Makes sure that there is
    1) Either HTTP or HTTPS in the URL
    2) There is a trailing slash

    and makes then sure that the URL resolves to an ROC deployment
    """

    if not (("http://" in url) or ("https://" in url)):
        raise InvalidInstanceUrlError(
            "Your instance URL must contain http:// or https://"
        )

    if not url[-1] == "/":
        url += "/"

    try:
        test_url = urljoin(url, "db/_all_dbs/")
        req = requests.get(test_url)
        if not req.ok:
            raise InvalidInstanceUrlError(
                "Testing the instance URL failed.\
                 Make sure that you only provide the base URL and not any API endpoint such as `/db` or `/db/eln`"
            )
    except Exception as execpt:  # pylint:disable=broad-except
        raise InvalidInstanceUrlError("Testing the instance URL failed") from execpt

    return url
