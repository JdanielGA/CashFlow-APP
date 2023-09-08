# Desc: Import the necessary libraries and modules to create the autentification middleware.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi import APIRouter, HTTPException, status, Depends
from dotenv import load_dotenv
import os

from datetime import datetime, timedelta
from typing import Union

from jose import jwt, JWTError
from services.login import LoginService
from services.users import UserService

# Desc: Charge the environment variables.
load_dotenv()

# Desc: Variable for the secret key.
SECRET_KEY = os.environ.get('SECRET_KEY')

# Desc: APIRouter instance.
authentication_router = APIRouter()

# Desc: Set up the OAuth2 scheme for the user to use.
oauth2_scheme = OAuth2PasswordBearer('/token')

#Desc: Funtion to check the login.
def login(email: str, password: str):
    user_data = LoginService.login(email, password)
    if user_data is None:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    elif user_data is False:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    else:
        return user_data
    
# Desc: Funtion to create the access token.
def create_access_token(data: dict, time_expire: Union[datetime, None] = None):
    to_encode = data.copy()
    if time_expire is None:
        time_expire = datetime.utcnow() + timedelta(hours=1)
    else:
        time_expire = datetime.utcnow() + time_expire
    to_encode.update({'exp': time_expire})
    token_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return token_jwt

# Desc: Function to get the current user.
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = token_decode.get('sub')
        if user_id is None:
            raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    user = UserService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# Desc: Function to get the status of the user.
def get_user_status(user: dict = Depends(get_current_user)):
    if user.status == False:
        raise HTTPException(status_code=403, detail='User is inactive')
    return user

# Desc: Function to get the role of the user.
def get_user_role(id: int = Depends(get_current_user)):
    return id.role
    
# Desc: Function to create the scope of the role.
def get_user_scope(authorize: str = SecurityScopes(['admin', 'user', 'guest'])):
    if 'Admin' in authorize.scopes:
        return 'Admin'
    elif 'User' in authorize.scopes:
        return 'User'
    elif 'Guest' in authorize.scopes:
        return 'Guest'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid role')

# Desc: Function to user login.
@authentication_router.get('/login/user')
def user_login(user: dict = Depends(get_user_status)):
    return user

# Desc: Create a funtion to get the token.
@authentication_router.post('/token')
def token_generator(form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = login(form_data.username, form_data.password)
    access_token_expires = timedelta(hours=1)
    access_token_jwt = create_access_token({'sub': user_data.id}, time_expire=access_token_expires)
    return {'access_token': access_token_jwt, 'token_type': 'bearer'}
