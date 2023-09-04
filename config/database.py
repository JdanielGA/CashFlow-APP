# Desc: Import the necessary libraries and modules to create the database connection.
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Desc: Create the database path and the name.
sqlite_file_name = '../database/database.sqlite'

# Desc: Path to the directory where the database is located.
database_dir = os.path.dirname(os.path.realpath(__file__))

# Desc: Create the database URL.
database_url = f'sqlite:///{os.path.join(database_dir, sqlite_file_name)}'

# Desc: Create the database engine.
engine = create_engine(database_url, echo=True)

# Desc: Create the database session.
Database_session = sessionmaker(bind=engine)

# Desc: Create the base class for the database tables.
Base_database = declarative_base()