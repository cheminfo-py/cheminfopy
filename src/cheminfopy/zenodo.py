"""Helpers for uploading a cheminfo zip export to Zenodo."""
import json
import os
import shutil
import tempfile
import time
from glob import glob
from pathlib import Path
from typing import Callable, Optional

import natsort
import requests
from loguru import logger

_ZENODO_TIMEOUT = os.getenv("ZENODO_TIMEOUT", 0.3)


def _make_clean_sample_dirs(sample_files, outdir, sample_json_callback: Optional[Callable] = None):
    toc = []
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    for i, file in enumerate(sample_files):
        this_id = "{:03d}".format(i)
        sample = Path(file)
        shutil.copytree(sample.parent, os.path.join(outdir, f"sample_{this_id}"))
        toc.append({"kind": "sample", "id": this_id})

    all_index_files = glob(os.path.join(outdir, "*", "sample.json"))

    for index in all_index_files:
        # hack because the Zenodo view currently assumes index.json and spectra on the top level
        with open(index, "r") as handle:
            d = json.load(handle)
            d.update(d["$content"])
            if sample_json_callback is not None:
                d = sample_json_callback(d)

        with open(os.path.join(Path(index).parent, "index.json"), "w") as handle:
            json.dump(d, handle)

    with open(os.path.join(outdir, "_toc.json"), "w") as handle:
        json.dump(toc, handle)
    return toc


def _compile_samples(basefolder):
    all_samples = natsort.natsorted(glob(os.path.join(basefolder, "*", "*", "sample.json")))
    return all_samples


def _upload_to_zenodo(folder, deposition_number: int, token: str, sandbox: bool = True):
    params = {"access_token": token}
    headers = {"Content-Type": "application/json"}
    base_url = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"

    try:
        r = requests.get(
            f"{base_url}/api/deposit/depositions/{deposition_number}", params=params, json={}
        )
        metadata = r.json()["metadata"]
        sandbox_string = "&sandbox={sandbox}" if sandbox else ""
        metadata[
            "description"
        ] = f'<p>Visualize the data in this dataset: <a href="https://www.c6h6.org/zenodo/record/?id={deposition_number}{sandbox_string}">open entry</a>.</p>'

        data = {"metadata": metadata}

        new_version = r.json()["links"]["latest_draft"]
    except Exception as e:
        logger.exception(e)

    r = requests.put(
        f"{base_url}/api/deposit/depositions/{deposition_number}",
        params={"access_token": token},
        data=json.dumps(data),
        headers=headers,
    )

    r = requests.get(f"{new_version}", params=params, json={})

    bucket_url = r.json()["links"]["bucket"]

    all_files = [
        p for p in glob(os.path.join(folder, "**"), recursive=True) if Path(p).suffix != ""
    ]
    filenames = [f.replace(f"{folder}/", "") for f in all_files]
    files = dict(zip(filenames, all_files))

    # We pass the file object (fp) directly to the request as the 'data' to be uploaded.
    # The target URL is a combination of the buckets link with the desired filename seperated by a slash.
    for k, v in files.items():
        with open(v, "rb") as fp:
            r = requests.put(
                "%s/%s" % (bucket_url, k),
                data=fp,
                # No headers included in the request, since it's a raw byte request
                params=params,
            )
        r.json()
        time.sleep(_ZENODO_TIMEOUT)


def upload_to_zenodo(
    extracted_zip_dir,
    deposition_number: int,
    token: str,
    sandbox: bool = True,
    delete_existing_files: bool = True,
    sample_json_callback: Optional[Callable] = None,
):
    """Upload a cheminfo zip export to Zenodo.
    Note that we assume that you already clicked on "new version" in the Zenodo UI.

    Args:
        extracted_zip_dir (str): Path to the extracted zip export
        deposition_number (int): Zenodo deposition number
        token (str): Zenodo access token
        sandbox (bool): Use the sandbox API
        delete_existing_files (bool): Delete all files from the draft deposition before uploading
        sample_json_callback (Callable): Callback function to modify the sample.json file before uploading
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        logger.debug(f"Using temporary directory {tmpdir} to compile samples")
        all_samples = _compile_samples(extracted_zip_dir)
        _make_clean_sample_dirs(all_samples, tmpdir, sample_json_callback)
        logger.debug(f"Done compiling samples")
        if delete_existing_files:
            logger.debug(f"Deleting existing files from Zenodo draft")
            depositions_url = (
                f"https://sandbox.zenodo.org/api/deposit/depositions/{deposition_number}"
                if sandbox
                else f"https://zenodo.org/api/deposit/depositions/{deposition_number}"
            )
            delete_files_from_draft(depositions_url, token)
        logger.debug(f"Uploading to Zenodo")
        _upload_to_zenodo(tmpdir, deposition_number, token, sandbox)


def delete_files_from_draft(depositions_url, token):
    """Delete all files from a draft deposition.

    Args:
        depositions_url (str): URL to the draft deposition
        token (str): Zenodo access token
    """
    try:
        r = requests.get(depositions_url, params={"access_token": token})
    except Exception as e:
        logger.exception(f"Could not get draft deposition due to {e}")
    files = r.json()["files"]
    num_files = len(files)
    logger.info(f"Deleting {num_files} files from {depositions_url}")
    while num_files > 0:
        for file in files:
            try:
                requests.delete(file["links"]["self"], params={"access_token": token})
            except Exception as e:
                logger.exception(f"Error deleting file {file['links']['self']} with error {e}")

            time.sleep(_ZENODO_TIMEOUT)
        try:
            r = requests.get(depositions_url, params={"access_token": token})
            files = r.json()["files"]
            num_files = len(files)
        except Exception as e:
            logger.exception(f"Error getting draft with error {e}")
        time.sleep(_ZENODO_TIMEOUT * 2)
