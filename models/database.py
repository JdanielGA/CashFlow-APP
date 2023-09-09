# Desc: Import necessary libraries and modules to create the database model.
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

# Desc: Import components from my own modules to create the user model.
from models.roles import Categories
from config.database import Base

# Desc: Create the database model
class DatabaseModel(Base):

    __tablename__ = 'database'

    ref = Column(Integer, primary_key=True, index=True)
    category = Column(Enum(Categories), nullable=False)
    tin = Column(Integer, primary_key=True, index=True, unique=True)
    dv = Column(Integer)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    self_retainer = Column(Boolean, nullable=False)
    ciium = Column(Integer, nullable=False)
    ciius = Column(Integer, nullable=True)
    ciiut = Column(Integer, nullable=True)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    city = Column(String, nullable=False)
    address = Column(String, nullable=False)
    contact_name = Column(String, nullable=True)
    contact_number = Column(String, nullable=True)
    created_date = Column(String, nullable=False)
