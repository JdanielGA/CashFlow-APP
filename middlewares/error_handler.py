# Desc: Import the necessary libraries to create the error handler middleware.
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, requests, Response
from fastapi.responses import JSONResponse as JSONR

# Desc: Creation of the error handler middleware.
class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: requests, call_next) -> Response | JSONR:
        try:
            return await call_next(request)
        except Exception as e:
            return JSONR(
                status_code=500,
                content={
                    'message': 'Internal Server Error',
                    'detail': str(e)
                }
            )