from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from app.users import UsersDB
from fastapi import HTTPException


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

@login_router.get('/login/user')
def user_login(token: str = Depends(oauth2_scheme)):
    return {'user': 'User1', 'status': 'logged'}

@login_router.post('/token')
def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = login(form_data.username, form_data.password)
    print(user)
    return {'access_token': 'test_tocken', 'token_type': 'bearer'}