from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from ..enums import PassportElementErrorType
from .passport_element_error import PassportElementError


class PassportElementErrorSelfie(PassportElementError):
    """
    Represents an issue with the selfie with a document. The error is considered resolved when the file with the selfie changes.

    Source: https://core.telegram.org/bots/api#passportelementerrorselfie
    """

    source: Literal[PassportElementErrorType.SELFIE] = PassportElementErrorType.SELFIE
    """Error source, must be *selfie*"""
    type: str
    """The section of the user's Telegram Passport which has the issue, one of 'passport', 'driver_license', 'identity_card', 'internal_passport'"""
    file_hash: str
    """Base64-encoded hash of the file with the selfie"""
    message: str
    """Error message"""

    if TYPE_CHECKING:
        # DO NOT EDIT MANUALLY!!!
        # This section was auto-generated via `butcher`

        def __init__(
            __pydantic__self__,
            *,
            source: Literal[PassportElementErrorType.SELFIE] = PassportElementErrorType.SELFIE,
            type: str,
            file_hash: str,
            message: str,
            **__pydantic_kwargs: Any,
        ) -> None:
            # DO NOT EDIT MANUALLY!!!
            # This method was auto-generated via `butcher`
            # Is needed only for type checking and IDE support without any additional plugins

            super().__init__(
                source=source, type=type, file_hash=file_hash, message=message, **__pydantic_kwargs
            )
