# Desc: Import the necessary libraries and modules to create the app routers.
from fastapi import APIRouter, Path, Depends, HTTPException
from config.database import Database_session
from models.database import DatabaseModel
from schemas.database import DatabaseSchema
from services.database import DatabaseService
from typing import List


# Desc: Create a instance of the APIRouter class.
database_router = APIRouter()

# Desc: Create a function to get the records from the database calling the service.
@database_router.get('/database', tags=['Database'], response_model=List[DatabaseSchema], status_code=200)
def get_all_records():
    try:
        db = Database_session()
        list_records = DatabaseService(db).get_all_records()
        return list_records
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to create a new record in the database calling the service.
@database_router.post('/database', tags=['Database'], response_model=dict,  status_code=201)
def create_record(database_schema: DatabaseSchema):
    try:
        db = Database_session()
        DatabaseService(db).create_record(database_schema)
        return {'message': 'Record created successfully.'}
    
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
