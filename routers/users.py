# Desc: Import the necessary libraries and modules to create the user routers.
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import SecretStr
from typing import List

# Desc: Import components from my own modules to create the user routers.
from routers.login import oauth2_scheme, get_current_active_user_role
from schemas.users import UserSchema, UserUpdateSchema, PasswordUpdateSchema
from config.database import SessionLocal
from services.users import UserService
from models.users import UserModel

# Desc: Instance of the APIRouter class.
users_router = APIRouter()

# Desc: Function to get all users calling the service.
@users_router.get('/users', tags=['Users'], status_code=200, response_model=List[UserSchema], summary='Get all users', dependencies=[Depends(oauth2_scheme)])
def get_all_users(role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        users = UserService(db).get_all_users()
        if not users:
            return JSONResponse(status_code=404, content={'message': 'Users database is empty.'})
        return users
    except  Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')
    
# Desc: Function to get a user by ID number calling the service.
@users_router.get('/users/{id_number}', tags=['Users'], status_code=200, response_model=UserSchema, summary='Get a user by ID number', dependencies=[Depends(oauth2_scheme)])
def get_user_by_id_number(id_number: int = Path(..., description='User ID number'), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        user = UserService(db).get_user_by_id_number(id_number)
        if not user:
            return JSONResponse(status_code=404, content={'message': 'Error: The user does not exist.'})
        return user
    except  Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')

# Desc: Function to create a new user calling the service.
@users_router.post('/users/create', tags=['Users'], status_code=201, response_model=UserSchema, summary='Create a new user', dependencies=[Depends(oauth2_scheme)])
def create_user(user: UserSchema = Depends(), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        check_id_number = UserService(db).get_user_by_id_number(user.id_number)
        check_company_id = UserService(db).get_user_by_company_id(user.company_id)
        check_email = UserService(db).get_user_by_email(user.email)
        if check_id_number:
            return JSONResponse(status_code=400, content={'message': 'Error: The user ID number already exists.'})
        if check_company_id:
            return JSONResponse(status_code=400, content={'message': 'Error: The user company ID already exists.'})      
        if check_email:
            return JSONResponse(status_code=400, content={'message': 'Error: The user email already exists.'})    
        new_user = UserService(db).create_user(user)
        return JSONResponse(status_code=201, content={'message': 'User created successfully.', 'email': new_user.email, 'position': new_user.position, 'role': new_user.role.value})      
    except IntegrityError as e:
        return JSONResponse(status_code=400, content={'message': f'Error: {e}. The user already exists.'})
    except  Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')

# Desc: Function to update a user calling the service.
@users_router.put('/users/update/{id_to_search}', tags=['Users'], status_code=200, response_model=UserUpdateSchema, summary='Update a user', dependencies=[Depends(oauth2_scheme)])
def update_user(id_to_search: int = Path(..., description='User ID number'), user: UserUpdateSchema = Depends(), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        user_updated = UserService(db).update_user(id_to_search, user)
        if user_updated is None:
            return JSONResponse(status_code=404, content={'message': 'Error: The user does not exist.'})
        if not user_updated:
            return JSONResponse(status_code=400, content={'message': 'Error: The user company ID or email already exists.'})
        return JSONResponse(status_code=200, content={'message': 'User updated successfully.'})
    except IntegrityError as e:
        return JSONResponse(status_code=400, content={'message': f'Error: {e}. The user already exists.'})
    except  Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')
    
# Desc: Function to update a user password calling the service.
@users_router.put('/users/change/password', tags=['Users'], status_code=200, response_model=PasswordUpdateSchema, summary='Update a user password', dependencies=[Depends(oauth2_scheme)])
def update_user_password(email: str = Query(..., description='User email', min_length=5, max_length=50), old_password: SecretStr = Query(..., description='User old password', min_length=1, max_length=50), new_password: SecretStr = Query(..., description='User new password', min_length=1, max_length=50), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin', 'User', 'Guest']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        user_updated = UserService(db).update_user_password(email, old_password.get_secret_value(), new_password.get_secret_value())
        if user_updated is None:
            return JSONResponse(status_code=404, content={'message': 'Error: The user does not exist.'})
        if not user_updated:
            return JSONResponse(status_code=400, content={'message': 'Error: The user old password is incorrect.'})
        return JSONResponse(status_code=200, content={'message': 'User password updated successfully.'})
    except IntegrityError as e:
        return JSONResponse(status_code=400, content={'message': f'Error: {e}. The user already exists.'})
    except  Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')
    
# Desc: Function to delete a user calling the service.
@users_router.delete('/users/delete/{id_number}', tags=['Users'], status_code=200, summary='Delete a user', dependencies=[Depends(oauth2_scheme)])
def delete_user(id_number: int = Path(..., description='User ID number'), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        user_deleted = UserService(db).delete_user(id_number)
        if user_deleted is None:
            return JSONResponse(status_code=404, content={'message': 'Error: The user does not exist.'})
        return JSONResponse(status_code=200, content={'message': 'User deleted successfully.'})
    except  Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')



# # Desc: Function to test the login.
# @users_router.post('/users/login', tags=['Users'], status_code=200, response_model=UserSchema, summary='Login a user')
# def login_user(email: str = Query(..., description='User email', min_length=5, max_length=50), password: SecretStr = Query(..., description='User password', min_length=1, max_length=50)):
#     try:
#         db = SessionLocal()
#         user = UserService(db).login_user(email, password.get_secret_value())
#         if not user:
#             return JSONResponse(status_code=404, content={'message': 'Error: The user does not exist.'})
#         return user
#     except  Exception as e:
#         return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
#     except:
#         raise HTTPException(status_code=500, detail='Internal server error.')