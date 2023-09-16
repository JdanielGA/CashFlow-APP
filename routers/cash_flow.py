# Desc: Import the necessary libraries and modules to create the Cash Flow routers.
from fastapi import APIRouter, HTTPException, Path, Depends, Query
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from pydantic import SecretStr
from typing import List

# Desc: Import components from my own modules to create the Cash Flow routers.
from routers.login import oauth2_scheme, get_current_active_user_role
from schemas.cash_flow import CashFlowSchema
from services.cash_flow import CashFlowServices
from config.database import SessionLocal

# Desc: Instance of the APIRouter class.
cash_flow_router = APIRouter()

# Desc: Function to get all the Cash Flow records calling the service class.
@cash_flow_router.get('/cash_flow/get', tags=['Cash Flow'], response_model=List[CashFlowSchema])
def get_all_cash_flow_records():
    try:
        db = SessionLocal()
        records = CashFlowServices(db).get_all()
        if not records:
            return JSONResponse(status_code=404, content={'message': 'There are no records in the database.'})
        return records
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': f'Error: {e}.'})
    except:
        raise HTTPException(status_code=500, detail='Internal server error.')