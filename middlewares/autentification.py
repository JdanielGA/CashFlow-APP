from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from dotenv import load_dotenv
from jose import jwt, JWTError
from app.users import UsersDB
from typing import Union
import os

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

login_router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer('/token')


def login (email: str, password: str):
    comprobation = UsersDB().login(email, password)
    if comprobation is None:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    elif comprobation is False:
        raise HTTPException(status_code=401, detail='Invalid credentials', headers={'WWW-Authenticate': 'Bearer'})
    else:   
        return comprobation

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
        print(username)
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


@login_router.get('/login/user')
def user_login(user: dict = Depends(get_user_disable_current)):
    return {'id': user['id'], 'first_name': user['first_name'], 'last_name': user['last_name'], 'email': user['email']}

@login_router.post('/token')
def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = login(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_access_token({'sub': user['id']}, time_expire=access_token_expires)
    return {'access_token': access_token_jwt, 'token_type': 'bearer'}