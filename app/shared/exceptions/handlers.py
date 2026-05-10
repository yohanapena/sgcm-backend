from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from .errors import (
    SGCMError,
    SGCMNotFoundError,
    SGCMConflictError,
    SGCMValidationError,
    SGCMAuthError,
)


def _error_response(status_code: int, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": exc.__class__.__name__,
            "detail": getattr(exc, "detail", str(exc) or "Ocurrió un error"),
        },
    )


def registrar_handlers(app: FastAPI) -> None:
    @app.exception_handler(SGCMNotFoundError)
    async def not_found_handler(request: Request, exc: SGCMNotFoundError):
        return _error_response(HTTP_404_NOT_FOUND, exc)

    @app.exception_handler(SGCMConflictError)
    async def conflict_handler(request: Request, exc: SGCMConflictError):
        return _error_response(HTTP_409_CONFLICT, exc)

    @app.exception_handler(SGCMValidationError)
    async def validation_handler(request: Request, exc: SGCMValidationError):
        return _error_response(HTTP_400_BAD_REQUEST, exc)

    @app.exception_handler(SGCMAuthError)
    async def auth_handler(request: Request, exc: SGCMAuthError):
        return _error_response(HTTP_401_UNAUTHORIZED, exc)

    @app.exception_handler(SGCMError)
    async def domain_error_handler(request: Request, exc: SGCMError):
        return _error_response(HTTP_400_BAD_REQUEST, exc)

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        return _error_response(HTTP_500_INTERNAL_SERVER_ERROR, exc)
