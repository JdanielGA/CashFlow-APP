'''
Estoy usando python, fastapi, sqlalchemy, werkzeug más PyJWT Para crear una App y Quiero crear un “Router” para el iniciar sesión de mi aplicación, anteriormente se uso este código para crear almacenar las contraseñas:

# Desc: Import the necessary libraries and modules to create the users model.
from config.database import Base_database
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

# Desc: Create the users model.
class UsersModel(Base_database):

    __tablename__ = 'users'

    company_id = Column(Integer, primary_key=True, unique=True)
    id = Column(Integer, ForeignKey('database.nit'), primary_key=True, unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    position = Column(String(50))
    company_phone = Column(Integer)
    corporate_email = Column(String(50))
    password_hash = Column(String)
    permission_level = Column(Integer)
    database = relationship('DatabaseModel', back_populates='users')

    # Desc: Create a funtion to generate the password hash.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Desc: Create a funtion to check the password hash.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

Y se almacenaban en la tabla "users" de la base de datos de esta manera:

# Desc: Import the necessary libraries and modules to create the user services.
from sqlalchemy import not_
from models.users import UsersModel
from schemas.users import UsersSchema

# Desc: Create a class to manage the users services.
class UserService:
    def __init__(self, db) -> None:
        self.db = db

    # Desc: Create a funtion to create a new user implementing the password hash with the set_password funtion from the model.
    def create_user(self, user: UsersSchema):
        new_user = UsersModel(
            company_id=user.company_id,
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            position=user.position,
            company_phone=user.company_phone,
            corporate_email=user.corporate_email,
            permission_level=user.permission_level
        )
        new_user.set_password(user.password_hash)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

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

¿Cómo lo quedaría el código?

'''