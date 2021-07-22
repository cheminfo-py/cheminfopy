# -*- coding: utf-8 -*-
"""Custom error types for cheminfopy"""

__all__ = [
    "InvalidAttachmentTypeError",
    "InvalidSourceError",
    "AuthenticationError",
    "InvalidInstanceUrlError",
    "RequestFailed",
]


class InvalidAttachmentTypeError(ValueError):
    """Raised in case of incompatible attachment type"""


class InvalidSourceError(ValueError):
    """Raised if a "data_type"/"source" key does not match the schema"""


class AuthenticationError(ValueError):
    """Raised if authentication fails"""


class InvalidInstanceUrlError(ValueError):
    """Raised if the provided instance URL seems invalid"""


class RequestFailed(ValueError):
    """Raised if the request failed"""
