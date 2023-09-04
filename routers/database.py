# Desc: Import the necessary libraries and modules to create the app routers.
from fastapi import APIRouter, Path, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from config.database import Database_session
from models.database import DatabaseModel
from schemas.database import DatabaseSchema
from services.database import DatabaseService
from typing import List


# Desc: Create a instance of the APIRouter class.
database_router = APIRouter()

# Desc: Create a function to get the records from the database calling the service.
@database_router.get('/database', tags=['Database'], response_model=List[DatabaseSchema], status_code=200, summary='Get all records - Obtener todos los registros.')
def get_all_records():
    try:
        db = Database_session()
        record_list = DatabaseService(db).get_all_records()
        # Desc: Determine if the record_list is empty.
        if record_list:
            return record_list
        else:
            return JSONResponse(status_code=404, content={'message': 'Records not found.'})
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to get a record by nit from the database calling the service.
@database_router.get('/database/nit/{nit}', tags=['Database'], response_model=DatabaseSchema, status_code=200, summary='Get record by nit - Obtener un registro por el nit.')
def get_record_by_nit(nit: int = Path(..., title='Nit', description='Nit of the record to get.')):
    try:
        db = Database_session()
        record = DatabaseService(db).get_record_by_nit(nit)
        if record:
            return record
        else:
            return JSONResponse(status_code=404, content={'message': 'Record not found.'})
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to get a record by name from the database calling the service.
@database_router.get('/database/name/{name}', tags=['Database'], response_model=DatabaseSchema, status_code=200, summary='Get record by name - Obtener un registro por el nombre.')
def get_record_by_name(name: str = Path(description='Name of the record to get.')):
    try:
        db = Database_session()
        record = DatabaseService(db).get_record_by_name(name)
        if record:
            return record
        else:
            return JSONResponse(status_code=404, content={'message': 'Record not found.'})
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to get a record category from the database calling the service.
@database_router.get('/database/category/{category}', tags=['Database'], response_model=List[DatabaseSchema], status_code=200, summary='Get record by category - Obtener un registro por la categoría.')
def get_record__by_category(category: str = Path(..., description='Category of the record to get.')):
    try:
        db = Database_session()
        record_list = DatabaseService(db).get_record_category(category)
        if record_list:
            return record_list
        else:
            return JSONResponse(status_code=404, content={'message': 'Records not found.'})
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to create a new record (checking if not exits yet) in the database calling the service.
@database_router.post('/database/create', tags=['Database'], response_model=DatabaseSchema,  status_code=201, summary='Create record - Crear un registro.')
def create_record(category: str = Query(..., enum=['Cliente', 'Proveedor', 'Empleado', 'Otro']),database_schema: DatabaseSchema = Depends()):
    try:
        db = Database_session()
        record_nit = DatabaseService(db).get_record_by_nit(database_schema.nit)
        record_name = DatabaseService(db).get_record_by_name(database_schema.name)
        if record_nit or record_name:
            return JSONResponse(status_code=400, content={'message': 'Record already exists.'})
        else:
            DatabaseService(db).create_record(database_schema)
            return JSONResponse(status_code=201, content={'message': 'Record created successfully.'})
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to update a record from the database (without add the same name of other record) calling the service.
@database_router.put('/database/update/{nit}', tags=['Database'], response_model=DatabaseSchema, status_code=200, summary='Update record - Actualizar un registro.')
def update_record(nit: int = Path(..., title='Nit', description='Nit of the record to update.'),category: str = Query(..., enum=['Cliente', 'Proveedor', 'Empleado', 'Otro']), database_schema: DatabaseSchema = Depends()):
    try:
        db = Database_session()
        record_updated = DatabaseService(db).update_record(nit, database_schema)
        if record_updated:
            return JSONResponse(status_code=200, content={'message': 'Record updated successfully.'})
        else:
            return JSONResponse(status_code=404, content={'message': 'Record not found or name already exists.'})
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to delete a record from the database calling the service.
@database_router.delete('/database/delete/{nit}', tags=['Database'], response_model=dict, status_code=200, summary='Delete record - Eliminar un registro.')
def delete_record(nit: int = Path(..., title='Nit', description='Nit of the record to delete.')):
    try:
        db = Database_session()
        record_deleted = DatabaseService(db).delete_record(nit)
        if record_deleted:
            return {'message': 'Record deleted successfully.'}
        else:
            return {'message': 'Record not found.'}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
# Desc: Create a function to delete all records from the database calling the service.
@database_router.delete('/database/delete_all', tags=['Database'], response_model=dict, status_code=200, summary='Delete all records - Eliminar todos los registros.')
def delete_all_records():
    try:
        db = Database_session()
        DatabaseService(db).delete_all_records()
        return {'message': 'Records deleted successfully.'}
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
            
