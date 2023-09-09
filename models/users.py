# Desc: Import necessary libraries and modules to create the user model.
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

# Desc: Import components from my own modules to create the user model.
from config.database import Base
from models.roles import Roles

# Desc: Create the users model.
class UserModel(Base):

    __tablename__ = 'users'

    id_number = Column(Integer, primary_key=True, index=True)
    company_id = Column(String, unique=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    position = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(Roles))
    active_status = Column(Boolean)
    date_created = Column(String)

    # Desc: Funtion to generate the password hash.
    def generate_password(self, password):
        self.password = generate_password_hash(password)

    # Desc: Function to check the password hash.
    def check_password(self, password):
        return check_password_hash(self.password, password)