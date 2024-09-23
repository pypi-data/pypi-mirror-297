from logging import Logger
from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


def parse_code_format(code: int | None) -> str:
    default_code_digits = 3
    if code is None:
        return "X" * default_code_digits
    code = str(code)
    current_code_len = len(code)
    if current_code_len > default_code_digits:
        raise ValueError(f"Code must be less than {current_code_len} digits.")
    code = "0" * (default_code_digits - current_code_len) + code
    return code


class HuginnMuninnError(Exception):
    """base exception class"""
    api_ref = None
    interface_ref = None
    logger: Logger | None = None

    def __init__(
            self,
            interface_ref: int | None = None,
            generic_error_code: int | None = None,
            internal_error_code: int | None = None,
            detail: str = "",
    ):
        # Handle error codes format
        self.api_ref = parse_code_format(self.api_ref)
        self.interface_ref = parse_code_format(interface_ref)
        self.generic_error_code = parse_code_format(generic_error_code)
        self.internal_error_code = parse_code_format(internal_error_code)

        # Error detail and user message
        self.detail = detail

        # Build error code string
        self.full_error_code = "-".join(
            [self.api_ref, self.interface_ref, self.generic_error_code, self.internal_error_code]
        )
        super().__init__(self.full_error_code, self.detail)
        if self.logger:
            self.logger.error(f"Error: {self.full_error_code}")


class HuginnMuninnHTTPException(HuginnMuninnError):
    status_code: int
    user_message: str = ""

    def __init__(
            self,
            generic_error_code: int | None = None,
            detail: str = "",
            user_message: str | None = None,
            interface_ref: int | None = None,
            internal_error_code: int | None = None,
            status_code: int | None = None,
    ):
        super().__init__(
            generic_error_code=generic_error_code,
            detail=detail,
            interface_ref=interface_ref,
            internal_error_code=internal_error_code
        )
        self.user_message = user_message if user_message else self.user_message
        self.status_code = self.status_code if status_code is None else status_code

    @classmethod
    def fastapi_exception_handler(cls) -> dict[str, Any]:
        def exception_handler(_: Request, exc: HuginnMuninnHTTPException) -> JSONResponse:
            return JSONResponse(
                status_code=exc.status_code,
                content={
                    "error_code": exc.full_error_code,
                    "detail": exc.detail,
                    "user_message": exc.user_message,
                },
                headers=None
            )

        return {"exc_class_or_status_code": cls,
                "handler": exception_handler}
