"""Custom exceptions and error handlers."""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
from app.core.logging import logger


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, detail: str = None, code: str = None):
        self.message = message
        self.detail = detail or message
        self.code = code or "APP_ERROR"
        super().__init__(self.message)


class NotFoundError(AppException):
    """Resource not found error."""

    def __init__(self, resource: str, resource_id: str = None):
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(
            message=message,
            detail=message,
            code="NOT_FOUND"
        )


class ValidationError(AppException):
    """Validation error."""

    def __init__(self, message: str, field: str = None):
        detail = message
        if field:
            detail = f"Validation error for field '{field}': {message}"
        super().__init__(
            message=message,
            detail=detail,
            code="VALIDATION_ERROR"
        )


class DatabaseError(AppException):
    """Database operation error."""

    def __init__(self, message: str, operation: str = None):
        detail = message
        if operation:
            detail = f"Database {operation} failed: {message}"
        super().__init__(
            message=message,
            detail=detail,
            code="DATABASE_ERROR"
        )


class ServiceError(AppException):
    """External service error."""

    def __init__(self, service: str, message: str):
        super().__init__(
            message=f"{service} service error: {message}",
            detail=message,
            code="SERVICE_ERROR"
        )


def create_error_response(
    error: Union[str, Exception],
    status_code: int = 500,
    detail: str = None,
    code: str = None
) -> JSONResponse:
    """Create standardized error response."""
    if isinstance(error, AppException):
        return JSONResponse(
            status_code=status_code,
            content={
                "error": error.message,
                "detail": error.detail,
                "code": error.code
            }
        )

    error_message = str(error) if isinstance(error, Exception) else error
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error_message,
            "detail": detail or error_message,
            "code": code or "INTERNAL_ERROR"
        }
    )


async def app_exception_handler(request: Request, exc: AppException):
    """Handler for custom application exceptions."""
    logger.error(
        "app_exception",
        code=exc.code,
        message=exc.message,
        detail=exc.detail,
        path=request.url.path
    )

    # Map exception types to HTTP status codes
    status_map = {
        "NOT_FOUND": 404,
        "VALIDATION_ERROR": 422,
        "DATABASE_ERROR": 500,
        "SERVICE_ERROR": 503
    }

    status_code = status_map.get(exc.code, 500)

    return create_error_response(
        error=exc,
        status_code=status_code
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handler for HTTP exceptions."""
    logger.warning(
        "http_exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "detail": exc.detail,
            "code": f"HTTP_{exc.status_code}"
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for validation errors."""
    errors = exc.errors()
    logger.warning(
        "validation_error",
        errors=errors,
        path=request.url.path
    )

    # Extract field names and messages
    field_errors = [
        {
            "field": ".".join(str(loc) for loc in err["loc"][1:]),  # Skip 'body'
            "message": err["msg"],
            "type": err["type"]
        }
        for err in errors
    ]

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "detail": "Request validation failed. Check field errors.",
            "code": "VALIDATION_ERROR",
            "field_errors": field_errors
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handler for unhandled exceptions."""
    logger.error(
        "unhandled_exception",
        error=str(exc),
        error_type=type(exc).__name__,
        path=request.url.path
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later.",
            "code": "INTERNAL_ERROR"
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
