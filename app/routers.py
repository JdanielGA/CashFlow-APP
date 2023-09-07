# Desc: Import the FastAPI libraries and modules for the routers of the app.
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import SecretStr
from app.users import UsersDB
from typing import List, Dict
from middlewares.autentification import oauth2_scheme

# Desc: Create an instance of the APIRouter class.
users_router = APIRouter()

# Desc: Create a function to get all the users from the database calling the service.
@users_router.get('/users', tags=['Users'], response_model=List, summary='Get all the users - Obtener todos los usuarios.', dependencies=[Depends(oauth2_scheme)])
def get_users():
    users = UsersDB().get_recors()
    if users is not None:
        if len(users) > 0:
            return JSONResponse(status_code=200, content=users)
        
        return JSONResponse(status_code=404, content={'message': 'The database is empty.'})
    
    else:
        return JSONResponse(status_code=404, content={'message': 'The database did not exist but it was created.'})

# Desc: Create a function to get a user by id from the database calling the service.
@users_router.get('/users/id/{id}', tags=['Users'], response_model=Dict, summary='Get a user by id - Obtener un usuario por id.', dependencies=[Depends(oauth2_scheme)])
def get_user_by_id(id):
    try:
        user = UsersDB().get_user_by_id(id)
        if user is not None:
            return JSONResponse(status_code=200, content=user)
        
        return JSONResponse(status_code=404, content={'message': 'The user does not exist.'})
    #verify if the fiel id is no empty
    except ValueError:
        return JSONResponse(status_code=400, content={'message': 'The id field is empty.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Desc: Create a function to create a new user calling the service.
@users_router.post('/users/create', tags=['Users'], summary='Create a new user - Crear un nuevo usuario.', dependencies=[Depends(oauth2_scheme)])
def create_user(id, first_name, last_name, email, password: SecretStr, disabled: bool):
    try:
        id_comprobation = UsersDB().get_user_by_id(id)
        email_comprobation = UsersDB().get_user_by_email(email)

        if id_comprobation is not None:
            return JSONResponse(status_code=400, content={'message': 'The user id already exist.'})
        
        elif email_comprobation is not None:
            return JSONResponse(status_code=400, content={'message': 'The email already exist.'})
        
        new_user = UsersDB().create_user(id, first_name, last_name, email, password.get_secret_value(), disabled)
        return JSONResponse(status_code=201, content=new_user)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Desc: Create a function to login a user calling the service.
@users_router.post('/users/login', tags=['Users'], summary='Login a user - Iniciar sesión de un usuario.', dependencies=[Depends(oauth2_scheme)])
def login(email, password: SecretStr):
    try:
        user = UsersDB().login(email, password.get_secret_value())
        if user is None:
            return JSONResponse(status_code=404, content={'message': 'The user does not exist.'})
        elif user is False:
            return JSONResponse(status_code=401, content={'message': 'The password is incorrect.'})
        else:
            return JSONResponse(status_code=200, content={'message': 'The user was logged successfully.', 'user': user})
        
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))