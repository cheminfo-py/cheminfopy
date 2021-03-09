# -*- coding: utf-8 -*-
from pathlib import Path

DEFAULT_SOURCE_DICT = {
    "name": "cheminfopy",
    "url": "https://github.com/cheminfo-py/c6h6py",
    "doi": "",
    "uuid": "",
}


def _get_attachment_json(type, filename, source_dict=None):
    if source_dict is None:
        source_dict = DEFAULT_SOURCE_DICT
    else:
        for k, v in source_dict.items():
            assert (
                k in DEFAULT_SOURCE_DICT.keys()
            ), f"Allowed source keys ares {DEFAULT_SOURCE_DICT.keys()}"
            assert isinstance(v, str), "source values must be strings"

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
