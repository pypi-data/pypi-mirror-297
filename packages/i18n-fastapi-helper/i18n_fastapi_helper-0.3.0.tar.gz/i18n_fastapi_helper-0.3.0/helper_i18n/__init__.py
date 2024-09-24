from http import HTTPStatus
from typing import Any, Optional

from helper_i18n.typing import errors


class CustomException(Exception):
    def __init__(
        self,
        status_code: int,
        i18n_key: str,
        errors: Optional[errors] = None,
        **params: Any,
    ) -> None:
        self.status_code = status_code
        self.i18n_key = i18n_key
        self.errors = errors
        self.params = params
        super().__init__()

    def to_dict(self) -> dict[str, Any]:
        error = HTTPStatus(self.status_code).phrase
        return {
            "example": {
                "error": error,
                "message": self.i18n_key,
                "path": "/path",
                "errors": [],
            }
        }
