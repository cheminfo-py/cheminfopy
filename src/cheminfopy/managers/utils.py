# -*- coding: utf-8 -*-
from copy import deepcopy
from pathlib import Path

from ..constants import DEFAULT_SOURCE_DICT
from ..errors import InvalidSourceError


def _new_toc(toc, type, filename, metadata=None, source_dict=None):
    toc_copy = deepcopy(toc)
    if source_dict is None:
        source_dict = DEFAULT_SOURCE_DICT
    else:
        for key, value in source_dict.items():
            if key not in DEFAULT_SOURCE_DICT.keys():
                raise InvalidSourceError(
                    f"Invalid source key {key}. Allowed source keys ares {DEFAULT_SOURCE_DICT.keys()}"
                )
            if not isinstance(value, str):
                raise InvalidSourceError("Source values must be strings")

    extension = Path(filename).suffix.replace(".", "")
    append_dict = {
        "source": source_dict,
        extension: {"filename": f"spectra/{type}/{filename}"},
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
