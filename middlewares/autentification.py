from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from fastapi import APIRouter, HTTPException, status, Depends
from dotenv import load_dotenv
import os

from datetime import datetime, timedelta
from typing import Union

from jose import jwt, JWTError
from app.users import UsersDB

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer('/token')


def login (email: str, password: str):
    user_info = UsersDB().login(email, password)
    if user_info is None:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    elif user_info is False:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    else:   
        return user_info

def create_access_token(data: dict, time_expire: Union[datetime, None] = None):
    to_encode = data.copy()
    if time_expire is None:
        time_expire = datetime.utcnow() + timedelta(minutes=15)
    else:
        time_expire = datetime.utcnow() + time_expire
    to_encode.update({'exp': time_expire})
    token_jwt = jwt.encode(to_encode, key= SECRET_KEY, algorithm='HS256')
    return token_jwt

def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=['HS256'])
        username = token_decode.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    user = UsersDB().get_user_by_id(username)
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    return user

def get_user_disable_current(user: dict = Depends(get_user_current)):
    if user['disabled'] == True:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    return user

def get_current_role(id: str = Depends(get_user_current)):
    return id['role']

# Desc: Create a function to create the permissions scopes. Admin has full access, user has access only to the user zone.
def get_scopes(authorize: str = SecurityScopes(['admin', 'user', 'guest'])):
    if 'admin' in authorize.scopes:
        return 'admin'
    elif 'user' in authorize.scopes:
        return 'user'
    elif 'guest' in authorize.scopes:
        return 'guest'
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scopes.')


@login_router.get('/login/user')
def user_login(user: dict = Depends(get_user_disable_current)):
    return {'id': user['id'], 'first_name': user['first_name'], 'last_name': user['last_name'], 'email': user['email']}

@login_router.post('/token')
def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = login(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_access_token({'sub': user['id']}, time_expire=access_token_expires)
    return {'access_token': access_token_jwt, 'token_type': 'bearer'}

# Desc: Create a test route to check admin permissions.
@login_router.get('/test')
def test_route(role: str = Depends(get_current_role)):
    if role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not enough permissions.')
    return {'message': 'This is the admin zone.'}
    
# Desc: Create a test route to check user permissions, but the admin can access too.
@login_router.get('/test2')
def test_route(role: str = Depends(get_current_role)):
    if role not in ['admin', 'user']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not enough permissions.')
    return {'message': 'This is the user zone.'}

# Desc: Create a test route to check guest permissions, but the admin and user can access too.
@login_router.get('/test3')
def test_route(role: str = Depends(get_current_role)):
    if role not in ['admin', 'user', 'guest']:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not enough permissions.')
    return {'message': 'This is the guest zone.'}
