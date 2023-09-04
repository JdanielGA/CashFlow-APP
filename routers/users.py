# Desc: Import the necessary libraries and modules to create the user routers.
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from config.database import Database_session
from models.users import UsersModel
from schemas.users import UsersSchema
from services.users import UserService
from typing import List

# Desc: Create an instance of the APIRouter class.
users_router = APIRouter()

# Desc: Create a function to get the users records from the database calling the service.
@users_router.get('/users', tags=['Users'], response_model=List[UsersSchema], status_code=200, summary='Get all the users - Obtener todos los usuarios.')
def get_all_users():
    try:
        db = Database_session()
        users_list = UserService(db).get_all_users()
        if not users_list:
            return JSONResponse(status_code=404, content={'message': 'Users not found - Usuarios no encontrados.'})
        return users_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Desc: Create a function to get a user record by id from the database calling the service.
@users_router.get('/users/id/{id}', tags=['Users'], response_model=UsersSchema, status_code=200, summary='Get a user by id - Obtener un usuario por id.')
def get_user_by_id(id: int = Path(..., gt=0)):
    try:
        db = Database_session()
        user = UserService(db).get_user_by_id(id)
        if not user:
            return JSONResponse(status_code=404, content={'message': 'User not found - Usuario no encontrado.'})
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Desc: Create a function to get a user record by company id from the database calling the service.
@users_router.get('/users/company/{company_id}', tags=['Users'], response_model=UsersSchema, status_code=200, summary='Get a user by company id - Obtener un usuario por id de compañia.')
def get_user_by_company_id(company_id: int = Path(..., gt=0)):
    try:
        db = Database_session()
        user = UserService(db).get_user_by_company_id(company_id)
        if not user:
            return JSONResponse(status_code=404, content={'message': 'User not found - Usuario no encontrado.'})
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Desc: Create a function to create a new user record in the database calling the service.
@users_router.post('/users/create', tags=['Users'], response_model=UsersSchema, status_code=201, summary='Create a new user - Crear un nuevo usuario.')
def create_user(user: UsersSchema = Depends()):
    try:
        db = Database_session()
        new_record_id = UserService(db).get_user_by_id(user.id)
        if new_record_id:
            return JSONResponse(status_code=400, content={'message': 'User already exists - El usuario ya existe.'})
        new_user = UserService(db).create_user(user)
        return JSONResponse(status_code=201, content={'message': 'User created - Usuario creado.'})
    except IntegrityError as e:
        if "UNIQUE constraint failed: users.company_id" in str(e):
            return JSONResponse(status_code=400, content={'message': 'Company id already exists - El id de compañia ya existe.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Desc: Create a function to update a user record by company id in the database calling the service.
@users_router.put('/users/update/{company_id}', tags=['Users'], response_model=UsersSchema, status_code=200, summary='Update a user by company id - Actualizar un usuario por id de compañia.')
def update_user(company_id: int = Path(..., gt=0), user: UsersSchema = Depends()):
    try:
        db = Database_session()
        update_user = UserService(db).update_user(company_id, user)
        if not update_user:
            return JSONResponse(status_code=404, content={'message': 'User not found or the id already exists - Usuario no encontrado o el id ya existe.'})
        return JSONResponse(status_code=200, content={'message': 'User updated - Usuario actualizado.'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Desc: Create a function to delete a user record by company id in the database calling the service.
@users_router.delete('/users/delete/{company_id}', tags=['Users'], response_model=dict, status_code=200, summary='Delete a user by company id - Eliminar un usuario por id de compañia.')
def delete_user(company_id: int = Path(..., gt=0)):
    try:
        db = Database_session()
        user = UserService(db).delete_user(company_id)
        if not user:
            return JSONResponse(status_code=404, content={'message': 'User not found - Usuario no encontrado.'})
        return {'message': 'User deleted - Usuario eliminado.'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))