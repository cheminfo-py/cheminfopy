from pathlib import Path


def _get_attachment_json(revision, type, filename):
    extension = Path(filename).suffix
    return {
        "_rev": revision,
        "$content": {type: [{extension: {"filename": f"spectra/{type}/{filename}"}},]},
    }

