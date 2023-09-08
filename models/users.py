# Desc: Import the necessary libraries and modules to create the users model.
from config.database import Base_database
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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
    status = Column(Boolean)
    database = relationship('DatabaseModel', back_populates='users')

    # Desc: Create a funtion to generate the password hash.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Desc: Create a funtion to check the password hash.
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)