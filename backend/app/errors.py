from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

_CODE_BY_STATUS = {
    400: "VALIDATION_ERROR",
    401: "UNAUTHENTICATED",
    403: "FORBIDDEN",
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
    409: "CONFLICT",
    429: "RATE_LIMITED",
}


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(exc: HTTPException):
        code = _CODE_BY_STATUS.get(exc.code, "ERROR")
        return (
            jsonify({"error": {"code": code, "message": exc.description}}),
            exc.code or 500,
        )

    @app.errorhandler(Exception)
    def handle_unexpected_exception(exc: Exception):
        if app.testing:
            raise exc
        app.logger.exception("Unhandled exception")
        return (
            jsonify({"error": {"code": "INTERNAL", "message": "An internal error occurred."}}),
            500,
        )
