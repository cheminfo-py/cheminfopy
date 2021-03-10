# -*- coding: utf-8 -*-
from copy import deepcopy
from pathlib import Path

from ..constants import DEFAULT_SOURCE_DICT
from ..errors import InvalidSourceError


def _new_toc(toc, type, filename, source_dict=None):
    toc_copy = deepcopy(toc)
    if source_dict is None:
        source_dict = DEFAULT_SOURCE_DICT
    else:
        for k, v in source_dict.items():
            if k not in DEFAULT_SOURCE_DICT.keys():
                raise InvalidSourceError(
                    f"Invalid source key {k}. Allowed source keys ares {DEFAULT_SOURCE_DICT.keys()}"
                )
            if not isinstance(v, str):
                raise InvalidSourceError("Source values must be strings")

    extension = Path(filename).suffix.replace(".", "")
    toc_copy["$content"]["spectra"][type].append(
        {"source": source_dict, extension: {"filename": f"spectra/{type}/{filename}"}}
    )
    return toc_copy
