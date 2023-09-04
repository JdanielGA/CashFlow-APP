# Desc: Import the necessary libraries and modules to create the database model.
from config.database import Base_database
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


# Desc: Create the database model.
class DatabaseModel(Base_database):
    
    __tablename__ = 'database'

    category = Column(String(20))
    nit = Column(Integer, primary_key=True, unique=True)
    dv = Column(Integer)
    name = Column(String(50), primary_key=True, unique=True)
    last_name = Column(String(50))
    city = Column(String(50))
    adress = Column(String(255))
    email = Column(String(50))
    number = Column(Integer)
    self_retainer = Column(Boolean)
    main_activity = Column(Integer)
    second_activity = Column(Integer)
    third_activity = Column(Integer)
    contac_name = Column(String(50))
    contac_number = Column(Integer)
    users = relationship('UsersModel', back_populates='database')


