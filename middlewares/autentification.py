# Desc: Import the necessary libraries and modules to create the autentification middleware.
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from services.login import LoginService
from starlette.middleware.base import BaseHTTPMiddleware

# Desc: Create a class to create the autentification middleware.
class Autentification(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not Request.session.get('user'):
            if request.url.path not in ['/login', '/', '/docs', '/redoc', '/openapi.json']:
                raise HTTPException(status_code=401, detail='You must login to access this page - Debe iniciar sesión para acceder a esta página.')
        else:
            response = await call_next(request)
            return response
        