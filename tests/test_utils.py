# -*- coding: utf-8 -*-
"""Test cheminfopy utility functio"""
import pytest

from cheminfopy.errors import InvalidInstanceUrlError
from cheminfopy.managers.utils import sanitize_instance_url


def test_sanitize_instance_url():
    """Validate the validation"""
    with pytest.raises(InvalidInstanceUrlError):
        sanitize_instance_url("www.cheminfo")
    with pytest.raises(InvalidInstanceUrlError):
        sanitize_instance_url("cheminfo")

    with pytest.raises(InvalidInstanceUrlError):
        sanitize_instance_url("https://mydb.cheminfo.org/db/eln")

    assert sanitize_instance_url("https://mydb.cheminfo.org") == "https://mydb.cheminfo.org/"
