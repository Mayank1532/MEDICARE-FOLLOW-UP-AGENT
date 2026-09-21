import logging
import uuid
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError

logger = logging.getLogger(__name__)


def _request_id(request: Request) -> str:
    """Return the middleware request ID or create one if unavailable."""
    return getattr(request.state, "request_id", str(uuid.uuid4()))


async def app_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle expected application errors."""
    if not isinstance(exc, AppError):
        raise exc

    request_id = _request_id(request)

    logger.error(
        "application_error request_id=%s method=%s path=%s "
        "code=%s message=%s",
        request_id,
        request.method,
        request.url.path,
        exc.code,
        exc.message,
    )

    status_code = 404 if exc.code == "PATIENT_NOT_FOUND" else 500

    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.code,
            "message": exc.message,
            "request_id": request_id,
        },
    )


async def validation_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle invalid API request payloads."""
    if not isinstance(exc, RequestValidationError):
        raise exc

    request_id = _request_id(request)

    logger.warning(
        "validation_error request_id=%s method=%s path=%s errors=%s",
        request_id,
        request.method,
        request.url.path,
        exc.errors(),
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "VALIDATION_ERROR",
            "message": "The request data is invalid.",
            "request_id": request_id,
            "details": _safe_validation_errors(exc),
        },
    )


def _safe_validation_errors(
    exc: RequestValidationError,
) -> list[dict[str, Any]]:
    """Convert validation errors to JSON-safe dictionaries."""
    return [
        {
            "loc": list(error.get("loc", ())),
            "type": error.get("type", "validation_error"),
            "msg": error.get("msg", "Invalid request"),
        }
        for error in exc.errors()
    ]


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Handle unexpected application failures without exposing internals."""
    request_id = _request_id(request)

    logger.exception(
        "unexpected_error request_id=%s method=%s path=%s "
        "error_type=%s error=%s",
        request_id,
        request.method,
        request.url.path,
        type(exc).__name__,
        str(exc),
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_SERVER_ERROR",
            "message": (
                "The request could not be completed. "
                "Check the backend logs using the request ID."
            ),
            "request_id": request_id,
        },
    )
