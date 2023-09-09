# Desc: Import the necessary libraries and modules to create the login router.
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from fastapi.responses import Response
from dotenv import load_dotenv
from jose import jwt, JWTError
from typing import Annotated
import os

# Desc: Import components from my own modules to create the login router.
from services.users import UserService
from config.database import SessionLocal

# Desc: Instance of the APIRouter class.
login_router = APIRouter()

# Desc: Load the environment variables.
load_dotenv()

# Desc: Define the secret key path.
SECRET_KEY = os.environ.get('SECRET_KEY')

# Desc: instance of the OAuth2PasswordBearer class.
oauth2_scheme = OAuth2PasswordBearer('/token')

# Desc: Function to authenticate the user.
def authenticate_user(email: str, password: str):
    db = SessionLocal()
    user = UserService(db).login_user(email, password)
    if not user:
        return False
    return user

# Desc: Function to create the access token.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm='HS256')
    return encoded_jwt

# Desc: Function to get the current user.
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials.', headers={'WWW-Authenticate': 'Bearer'})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = UserService(db).get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

# Desc: Function to get the current active user.
async def get_current_active_user(current_user: dict = Depends(get_current_user)):
    if not current_user.active_status:
        raise HTTPException(status_code=400, detail='Inactive user.')
    return current_user

# Desc: Function to get the current active user role.
async def get_current_active_user_role(current_user: dict = Depends(get_current_user)):
    if not current_user.active_status:
        raise HTTPException(status_code=400, detail='Inactive user.')
    return current_user.role.value 

# Desc: Function to log in and issue access token.
@login_router.post('/token', tags=['Login'], status_code=200, summary='Sign in and issue the access token.')
async def login_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Incorrect email or password.', headers={'WWW-Authenticate': 'Bearer'})
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

# Desc: Function to log out the current user.
@login_router.post('/logout', tags=['Logout'], status_code=200, summary='Log out the current user.')
async def logout_user(response: Response):
    response.delete_cookie('access_token')
    return {'detail': 'Logged out.'}
    
# Desc: Check the active user and return the welcome message if the user is active.
@login_router.get('/login', tags=['Login'], status_code=200, summary='Test login', dependencies=[Depends(get_current_active_user)])
async def test_login(current_user: dict = Depends(get_current_user)):
    return {'message': f'Welcome {current_user.first_name} {current_user.last_name}', 'company_id': current_user.company_id, 'email': current_user.email, 'role': current_user.role}

# Desc: Function to test the permissions scopes(admin).
@login_router.get('/admin', tags=['Login'], status_code=200, summary='Test permissions scopes(admin)', dependencies=[Depends(oauth2_scheme)])
def admin_zone(role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        raise HTTPException(status_code=401, detail='Unauthorized.')
    return {'message': 'Welcome to the admin zone.'}

# Desc: Function to test the permissions scopes(user).
@login_router.get('/user', tags=['Login'], status_code=200, summary='Test permissions scopes(user)', dependencies=[Depends(oauth2_scheme)])
def user_zone(role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin', 'User']:
        raise HTTPException(status_code=401, detail='Unauthorized.')
    return {'message': 'Welcome to the user zone.'}

# Desc: Function to test the permissions scopes(guest).
@login_router.get('/guest', tags=['Login'], status_code=200, summary='Test permissions scopes(guest)', dependencies=[Depends(oauth2_scheme)])
def guest_zone(role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin', 'User', 'Guest']:
        raise HTTPException(status_code=401, detail='Unauthorized.')
    return {'message': 'Welcome to the guest zone.'}