# Desc: Import the necessary libraries and modules to create the database routers.
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import SecretStr
from typing import List

# Desc: Import components from my own modules to create the database routers.
from routers.login import oauth2_scheme, get_current_active_user_role
from schemas.database import DatabaseSchema, UpdateSchema
from services.database import DatabaseServices
from config.database import SessionLocal

# Desc: Instance of the APIRouter class.
database_router = APIRouter()

# Desc: Function to create a new database record calling the service class.
@database_router.post('/database/create', tags=['Database'], response_model=DatabaseSchema, summary='Create a new database record - Crear un nuevo registro en la base de datos.', dependencies=[Depends(oauth2_scheme)])
def create_new_database_record(database: DatabaseSchema = Depends(),role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin', 'User']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        check_tin = DatabaseServices(db).get_by_tin(database.tin)
        check_email = DatabaseServices(db).get_by_email(database.email)
        if check_tin:
            return JSONResponse(status_code=400, content={'message': 'The TIN already exists in the database. - El NIT ya existe en la base de datos.'})
        if check_email:
            return JSONResponse(status_code=400, content={'message': 'The email already exists in the database. - El correo electrónico ya existe en la base de datos.'})
        new_record = DatabaseServices(db).create(database)
        return JSONResponse(status_code=201, content={'message': 'The record was created successfully. - El registro fue creado exitosamente.'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')

# Desc: Function to get the database records calling the service class.
@database_router.get('/database/get', tags=['Database'], response_model=List[DatabaseSchema], summary='Get all the database records - Obtener todos los registros de la base de datos.', dependencies=[Depends(oauth2_scheme)])
def get_all_database_records(role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin', 'User']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:    
        db = SessionLocal()
        records = DatabaseServices(db).get_all()
        if not records:
            return JSONResponse(status_code=404, content={'message': 'There are no records in the database.'})
        return records
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')
    
# Desc: Function to update a database record by TIN calling the service class.
@database_router.put('/database/update/{tin_to_search}', tags=['Database'], response_model=UpdateSchema, summary='Update a database record by TIN - Actualizar un registro de la base de datos por NIT.', dependencies=[Depends(oauth2_scheme)])
def update_database_record_by_tin(tin_to_search: int = Path(..., title='TIN', description='TIN of the record to be updated. - NIT del registro a actualizar.', gt=0), database: UpdateSchema = Depends(), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        record_to_update = DatabaseServices(db).update_by_tin(tin_to_search, database)
        if record_to_update is None:
            return JSONResponse(status_code=404, content={'message': 'The record was not found. - El registro no fue encontrado.'})
        if not record_to_update:
            return JSONResponse(status_code=400, content={'message': 'The TIN or email already exists in the database. - El NIT o correo electrónico ya existe en la base de datos.'})
        return JSONResponse(status_code=200, content={'message': 'The record was updated successfully. - El registro fue actualizado exitosamente.'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')
    
# Desc: Function to eliminate a database record by TIN calling the service class.
@database_router.delete('/database/delete/{tin}', tags=['Database'], summary='Delete a database record by TIN - Eliminar un registro de la base de datos por NIT.', dependencies=[Depends(oauth2_scheme)])
def delete_database_record_by_tin(tin: int = Path(..., title='TIN', description='TIN of the record to be deleted. - NIT del registro a eliminar.', gt=0), role: str = Depends(get_current_active_user_role)):
    if role not in ['Admin']:
        return JSONResponse(status_code=403, content={'message': 'Error: You do not have permission to perform this action.'})
    try:
        db = SessionLocal()
        record_to_delete = DatabaseServices(db).delete_by_tin(tin)
        if not record_to_delete:
            return JSONResponse(status_code=500, content={'message': 'Internal server error.'})
        return JSONResponse(status_code=200, content={'message': 'The record was deleted successfully. - El registro fue eliminado exitosamente.'})
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')