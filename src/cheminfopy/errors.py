# -*- coding: utf-8 -*-
"""Custom error types for cheminfopy"""

__all__ = [
    "InvalidAttachmentTypeError",
    "InvalidSourceError",
    "AuthenticationError",
    "InvalidInstanceUrlError",
]


class InvalidAttachmentTypeError(ValueError):
    """Raised in case of incompatible attachment type"""


class InvalidSourceError(ValueError):
    """Raised if a "spectrum_type"/"source" key does not match the schema"""


class AuthenticationError(ValueError):
    """Raised if authentication fails"""


class InvalidInstanceUrlError(ValueError):
    """Raised if the provided instance URL seems invalid"""
