# Desc: Libraries and modules to create the database connection.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Desc: Create the database path (if the file does not exist, it will be created).
sqlite_file_name = '../database/data_store.sqlite'

# Desc: Directory where the database is located.
sqlite_dir = os.path.dirname(os.path.abspath(__file__))

#Desc: Create the database URL.
sqlite_url = f'sqlite:///{os.path.join(sqlite_dir, sqlite_file_name)}'

# Desc: Create the database engine.
engine = create_engine(sqlite_url, echo=True, connect_args={'check_same_thread': False})

# Desc: Create the database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Desc: Create the base class for the database.
Base = declarative_base()