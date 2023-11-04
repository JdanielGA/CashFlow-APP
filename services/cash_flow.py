# Desc: Import the necesary libraries and modules to create the Cash Flow services.
from sqlalchemy import not_

# Desc: Import components from my own modules to create the Cash Flow services.
from schemas.cash_flow import CashFlowSchema
from models.cash_flow import CashFlowModel

# Desc: Cash Flow services class.
class CashFlowServices:
    def __init__(self, db):
        self.db = db

    # Desc: Function to get all the Cash Flow records.
    def get_all(self):
        records = self.db.query(CashFlowModel).all()
        return records
    
    def get_by_ref_number(self, ref_number: str):
        record = self.db.query(CashFlowModel).filter(CashFlowModel.ref_number == ref_number).first()
        return record
    
    # Desc: Function to create a Cash Flow record.
    def create(self, cash_flow: CashFlowSchema):
        new_record = CashFlowModel(**cash_flow.model_dump())
        self.db.add(new_record)
        self.db.commit()
        self.db.refresh(new_record)
        return new_record