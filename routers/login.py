# Desc: Import the necessary libraries and modules to create the login router.
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from fastapi.responses import JSONResponse
from services.login import LoginService
from config.database import Database_session
from pydantic import SecretStr
from sqlalchemy import text

# Desc: Create an instance of the APIRouter class.
login_router = APIRouter()

# Desc: Create a function to login the user calling the service.
@login_router.post('/login', tags=['Login'], status_code=200, summary='Login - Iniciar sesión.')
async def login(user: str = Query(..., description='Corporate email - Correo corporativo.'), password: SecretStr = Query(..., description='Password - Contraseña.')):
    with Database_session() as session:
        login_service = LoginService(session)
        user = login_service.login(user, password.get_secret_value())
        if user:
            search_user_full_name = session.execute(text(f"SELECT first_name, last_name FROM users WHERE corporate_email = '{user.corporate_email}'")).fetchone()
            return JSONResponse(status_code=200, content={'message': 'Login successful - Inicio de sesión exitoso.',
                                                          'welcome': f'Bienvenido {search_user_full_name[0]} {search_user_full_name[1]}.'})
        else:
            raise HTTPException(status_code=401, detail='Incorrect user or password - Usuario o contraseña incorrectos.')