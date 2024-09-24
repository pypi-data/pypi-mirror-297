"""Simple error handling for fastapi using custom error classes."""

from typing import Any, Type

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Represents error details."""

    error: str = Field(description="error identifier")
    message: str = Field(description="error message")


class ErrorResponse(BaseModel):
    """Represents an error response."""

    detail: ErrorDetail = Field(description="details about the error")


ResponseModelDict = dict[int | str, dict[str, Any]]


class AppError(HTTPException):
    """An error occurred."""

    # Light wrapper around HTTPException that allows specifying status code via class property
    # and default message via docstring.
    # The Python class name is used as error identifier.

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    headers = None
    model = ErrorResponse

    def __init__(self, message: str | None = None, headers: dict[str, str] | None = None) -> None:
        """Initialize."""
        message = message if message is not None else self.__doc__
        detail = ErrorDetail(message=message, error=self.__class__.__name__).model_dump()
        headers = headers if headers is not None else self.headers
        super().__init__(status_code=self.status_code, detail=detail, headers=headers)

    @classmethod
    def response_model(cls) -> ResponseModelDict:
        """Generate response model."""
        return {cls.status_code: {"model": cls.model}}


class BadRequestError(AppError):
    """Bad request."""

    status_code = status.HTTP_400_BAD_REQUEST


class UnauthorizedError(AppError):
    """Unauthorized."""

    status_code = status.HTTP_401_UNAUTHORIZED


class PaymentRequiredError(AppError):
    """Payment required."""

    status_code = status.HTTP_402_PAYMENT_REQUIRED


class NotFoundError(AppError):
    """Not found."""

    status_code = status.HTTP_404_NOT_FOUND


class ForbiddenError(AppError):
    """Forbidden."""

    status_code = status.HTTP_403_FORBIDDEN


class MethodNotAllowedError(AppError):
    """Method not allowed."""

    status_code = status.HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptableError(AppError):
    """Not acceptable."""

    status_code = status.HTTP_406_NOT_ACCEPTABLE


class ProxyAuthenticationRequiredError(AppError):
    """Proxy authentication required."""

    status_code = status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED


class RequestTimeoutError(AppError):
    """Request timeout."""

    status_code = status.HTTP_408_REQUEST_TIMEOUT


class ConflictError(AppError):
    """Conflict."""

    status_code = status.HTTP_409_CONFLICT


class GoneError(AppError):
    """Gone."""

    status_code = status.HTTP_410_GONE


class LengthRequiredError(AppError):
    """Length required."""

    status_code = status.HTTP_411_LENGTH_REQUIRED


class PreconditionFailedError(AppError):
    """Precondition failed."""

    status_code = status.HTTP_412_PRECONDITION_FAILED


class RequestEntityTooLargeError(AppError):
    """Request entity too large."""

    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class RequestUriTooLongError(AppError):
    """Request URI too long."""

    status_code = status.HTTP_414_REQUEST_URI_TOO_LONG


class UnsupportedMediaTypeError(AppError):
    """Unsupported media type."""

    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE


class RequestedRangeNotSatisfiableError(AppError):
    """Requested range not satisfiable."""

    status_code = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE


class ExpectationFailedError(AppError):
    """Expectation failed."""

    status_code = status.HTTP_417_EXPECTATION_FAILED


class ImATeapotError(AppError):
    """I'm a teapot."""

    status_code = status.HTTP_418_IM_A_TEAPOT


class MisdirectedRequestError(AppError):
    """Misdirected request."""

    status_code = status.HTTP_421_MISDIRECTED_REQUEST


class UnprocessableEntityError(AppError):
    """Unprocessable entity."""

    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class LockedError(AppError):
    """Locked."""

    status_code = status.HTTP_423_LOCKED


class FailedDependencyError(AppError):
    """Failed dependency."""

    status_code = status.HTTP_424_FAILED_DEPENDENCY


class TooEarlyError(AppError):
    """Too early."""

    status_code = status.HTTP_425_TOO_EARLY


class UpgradeRequiredError(AppError):
    """Upgrade required."""

    status_code = status.HTTP_426_UPGRADE_REQUIRED


class PreconditionRequiredError(AppError):
    """Precondition required."""

    status_code = status.HTTP_428_PRECONDITION_REQUIRED


class TooManyRequestsError(AppError):
    """Too many requests."""

    status_code = status.HTTP_429_TOO_MANY_REQUESTS


class RequestHeaderFieldsTooLargeError(AppError):
    """Request header fields too large."""

    status_code = status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE


class UnavailableForLegalReasonsError(AppError):
    """Unavailable for legal reasons."""

    status_code = status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS


class InternalServerError(AppError):
    """Internal server error."""

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class HttpNotImplementedError(AppError):
    """Not implemented."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED


class BadGatewayError(AppError):
    """Bad gateway."""

    status_code = status.HTTP_502_BAD_GATEWAY


class ServiceUnavailableError(AppError):
    """Service unavailable."""

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class GatewayTimeoutError(AppError):
    """Gateway timeout."""

    status_code = status.HTTP_504_GATEWAY_TIMEOUT


class HttpVersionNotSupportedError(AppError):
    """HTTP version not supported."""

    status_code = status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED


class VariantAlsoNegotiatesError(AppError):
    """Variant also negotiates."""

    status_code = status.HTTP_506_VARIANT_ALSO_NEGOTIATES


class InsufficientStorageError(AppError):
    """Insufficient storage."""

    status_code = status.HTTP_507_INSUFFICIENT_STORAGE


class LoopDetectedError(AppError):
    """Loop detected."""

    status_code = status.HTTP_508_LOOP_DETECTED


class NotExtendedError(AppError):
    """Not extended."""

    status_code = status.HTTP_510_NOT_EXTENDED


class NetworkAuthenticationRequiredError(AppError):
    """Network authentication required."""

    status_code = status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED


def error_responses(*args: Type[AppError]) -> ResponseModelDict:
    """Generate dict of responses for errors."""
    responses = {}
    for cls in args:
        responses.update(cls.response_model())
    return responses


def error_responses_from_status_codes(
    *args: int, table: dict[int, Type[AppError]] | None = None
) -> ResponseModelDict:
    """Generate dict of responses for errors (from status codes)."""
    if table is None:
        table = default_errors_table()
    return error_responses(*(table[code] for code in args))


def default_errors_table() -> dict[int, Type[AppError]]:
    """Get mapping from status codes to exception classes."""
    return {
        400: BadRequestError,
        401: UnauthorizedError,
        402: PaymentRequiredError,
        403: ForbiddenError,
        404: NotFoundError,
        405: MethodNotAllowedError,
        406: NotAcceptableError,
        407: ProxyAuthenticationRequiredError,
        408: RequestTimeoutError,
        409: ConflictError,
        410: GoneError,
        411: LengthRequiredError,
        412: PreconditionFailedError,
        413: RequestEntityTooLargeError,
        414: RequestUriTooLongError,
        415: UnsupportedMediaTypeError,
        416: RequestedRangeNotSatisfiableError,
        417: ExpectationFailedError,
        418: ImATeapotError,
        421: MisdirectedRequestError,
        422: UnprocessableEntityError,
        423: LockedError,
        424: FailedDependencyError,
        425: TooEarlyError,
        426: UpgradeRequiredError,
        428: PreconditionRequiredError,
        429: TooManyRequestsError,
        431: RequestHeaderFieldsTooLargeError,
        451: UnavailableForLegalReasonsError,
        500: InternalServerError,
        501: HttpNotImplementedError,
        502: BadGatewayError,
        503: ServiceUnavailableError,
        504: GatewayTimeoutError,
        505: HttpVersionNotSupportedError,
        506: VariantAlsoNegotiatesError,
        507: InsufficientStorageError,
        508: LoopDetectedError,
        510: NotExtendedError,
        511: NetworkAuthenticationRequiredError,
    }
