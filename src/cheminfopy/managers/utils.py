# -*- coding: utf-8 -*-
from pathlib import Path
from ..constants import DEFAULT_SOURCE_DICT
from ..errors import InvalidSourceError


def _get_attachment_json(type, filename, source_dict=None):
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

    extension = Path(filename).suffix
    return {
        "$content": {
            type: [
                {
                    "source": source_dict,
                    extension: {"filename": f"spectra/{type}/{filename}"},
                },
            ]
        },
    }
